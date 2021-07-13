from datetime import timedelta, datetime
import ssl

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

import ldap3

import db
import const
import schemas
from database import models
from database.database import SessionLocal

if const.AUTH_LDAP_ENABLED:
    if const.AUTH_LDAP_SECURITY:
        ldap_tls_config=ldap3.Tls(validate=ssl.CERT_REQUIRED if const.AUTH_LDAP_SECURITY_VALID_CERTIFICATE else ssl.CERT_NONE)
    else:
        ldap_tls_config = False
    LDAP_SERVER = ldap3.Server(const.AUTH_LDAP_SERVER, const.AUTH_LDAP_PORT, get_info=ldap3.ALL, use_ssl=const.AUTH_LDAP_SECURITY=="SSL", tls=ldap_tls_config)
else:
    LDAP_SERVER = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def logging_middleware(request: Request, call_next):
    response = await call_next(request)
    logger.opt(depth=2).info(f"{request.method} {request.url} - Code: {response.status_code}")
    return response


async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error (Database error)", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# NON MIDDLEWARE MIDDLEWARISH THING


# Dependency
def get_db(request: Request):
    return request.state.db


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, const.SECRET_KEY, algorithm=const.ALGORITHM)
    return encoded_jwt


def retrieve_api_key(request: Request):
    return request.headers.get("X-API-Key", None)


def auth(token: str = Depends(oauth2_scheme), api_key: str = Depends(retrieve_api_key), sess: Session = Depends(get_db)):

    username = None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Attempt to authenticate using JWT
    try:
        payload = jwt.decode(token, const.SECRET_KEY, algorithms=[const.ALGORITHM])
        username: str = payload.get("sub")
    except PyJWTError:
        pass

    try:
        db_user_api_key = sess.query(models.UserAPIKey).filter_by(key=api_key).one()
        username = db_user_api_key.user.username
    except Exception:
        pass

    if username is None:
        raise credentials_exception

    user = schemas.User.from_orm(
        schemas.UserInDB(username=username, password="").from_db(sess)
    )
    if user is None:
        raise credentials_exception
    return user

AUTH_ENGINES: dict = {}

def authengine(name: str, sequence: int, enabled: bool):
    def decorator(f):
        AUTH_ENGINES[name] = {
            "function": f,
            "sequence": sequence,
            "enabled": enabled
        }

    return decorator

class Authentication(object):

    def __init__(self, username: str, password: str, sess: Session):
        self.username = username
        self.password = password
        self.sess = sess

    def login(self):
        user: schemas.UserInDB = False

        for engine in sorted(AUTH_ENGINES.keys(), key=lambda x: AUTH_ENGINES[x]["sequence"]):
            if not AUTH_ENGINES[engine]["enabled"]:
                continue
            try:
                user = AUTH_ENGINES[engine]["function"](self)
                logger.info("User %s logged in via the %s authentication engine" % (self.username, engine))
                break
            except Exception as err:
                logger.warning("Login failed for %s using the %s authentication engine: %s" % (self.username, engine, err))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    @authengine(name="builtin", sequence=10, enabled=const.AUTH_LOCAL_ENABLED)
    def _builtin(self):
        assert const.AUTH_LOCAL_ENABLED, "LOCAL authentication not enabled"
        user: schemas.UserInDB = schemas.UserInDB(username=self.username, password="").from_db(self.sess)

        # Verify password
        assert user and verify_password(self.password, user.password), "Invalid username or password"

        return  user

    @authengine(name="LDAP", sequence=20, enabled=const.AUTH_LDAP_ENABLED)
    def _ldap(self):
        assert const.AUTH_LDAP_ENABLED, "LDAP authentication not enabled"

        def _get_ldap_attr(ldapobj, attribute):
            attr = ldapobj["attributes"].get(attribute, None)
            if isinstance(attr, list):
                try:
                    return attr[0]
                except IndexError:
                    return None
            return attr

        ldap_auth = ldap3.ANONYMOUS
        ldap_user = None
        valid: bool = False
        if const.AUTH_LDAP_USER:
            if const.AUTH_LDAP_ACTIVEDIRECTORY:
                ldap_auth = ldap3.NTLM
            else:
                ldap_auth = ldap3.SIMPLE

        # Connect with binddn, if set, to search the user
        with ldap3.Connection(LDAP_SERVER, user=const.AUTH_LDAP_USER, password=const.AUTH_LDAP_PASSWORD, authentication=ldap_auth, read_only=True, auto_bind=ldap3.AUTO_BIND_NONE) as cn:
            if const.AUTH_LDAP_SECURITY == "TLS":
                cn.start_tls()
            try:
                assert cn.bind()
                logger.debug("LDAP system bind complete")
            except:
                logger.exception("Unable to connect/bind to LDAP server")
                raise
            # TODO find a parsing tool like python-ldap.filter.filter_format
            ldap_filter: str = const.AUTH_LDAP_FILTER % self.username
            ldap_attributes: list = ["cn", "mail"]

            if const.AUTH_LDAP_ACTIVEDIRECTORY:
                ldap_attributes.extend(["samAccountName", "givenName"])
            cn.search(search_base=const.AUTH_LDAP_BASE, search_filter=ldap_filter, attributes=ldap_attributes)
            assert len(cn.response) == 1, "Found %d LDAP users for the filter %s" % (len(cn.response), ldap_filter)
            ldap_user = cn.response[0].copy()

        logininfo: str = "%s\%s" % (const.AUTH_LDAP_DOMAIN, _get_ldap_attr(ldap_user, "samAccountName")) if const.AUTH_LDAP_ACTIVEDIRECTORY else ldap_user["dn"]
        with ldap3.Connection(LDAP_SERVER, user=logininfo, password=self.password, authentication=ldap3.NTLM if const.AUTH_LDAP_ACTIVEDIRECTORY else ldap3.SIMPLE, read_only=True, auto_bind=ldap3.AUTO_BIND_NONE) as cn:
            if const.AUTH_LDAP_SECURITY == "TLS":
                cn.start_tls()
            assert cn.bind(), "LDAP authentication failed for %s" % self.username
            cn.unbind()

        user: schema.UserInDB = schemas.UserInDB(username=self.username, password="").from_db(self.sess)
        if user:
            user.full_name = _get_ldap_attr(ldap_user, "givenName" if const.AUTH_LDAP_ACTIVEDIRECTORY else "cn")
            user.email = _get_ldap_attr(ldap_user, "mail")
            user.password = None
            db.user.update_user(self.sess, user)
        else:
            if not db.user.create_user(self.sess, models.User(
                    username=username,
                    password=None,
                    full_name=_get_ldap_attr(ldap_user, "givenName" if const.AUTH_LDAP_ACTIVEDIRECTORY else "cn"),
                    email=_get_ldap_attr(ldap_user, "mail"),
                    role="user", # TODO: Map LDAP groups to roles
            )):
                raise HTTPException(status_code=400, detail="Could not create LDAP user")
            user: schema.UserInDB = schemas.UserInDB(username=self.username, password="").from_db(self.sess)
        return user
