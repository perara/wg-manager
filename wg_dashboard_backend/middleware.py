from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

import const
import schemas
from database import SessionLocal
import db.user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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


def auth(token: str = Depends(oauth2_scheme), sess: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, const.SECRET_KEY, algorithms=[const.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception
    user = schemas.User.from_orm(
        schemas.UserInDB(username=username, password="").from_db(sess)
    )
    if user is None:
        raise credentials_exception
    return user

