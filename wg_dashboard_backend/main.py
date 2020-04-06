import logging

from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.hasHandlers():
    sh = logging.StreamHandler()
    fmt = logging.Formatter(fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    sh.setFormatter(fmt)
    logger.addHandler(sh)
import pkg_resources
import uvicorn as uvicorn
from fastapi.staticfiles import StaticFiles
import databases
from sqlalchemy.orm import sessionmaker, Session
from starlette.responses import FileResponse, JSONResponse
import sqlalchemy
import const
from datetime import datetime, timedelta
import db.wireguard
import db.user
import jwt
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
import script.wireguard
import typing
import models
import schemas

database = databases.Database(const.DATABASE_URL)

engine = sqlalchemy.create_engine(
    const.DATABASE_URL, connect_args={"check_same_thread": False}
)

try:
    models.Base.metadata.create_all(engine)
except OperationalError as e:
    pass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, const.SECRET_KEY, algorithm=const.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), sess: Session = Depends(get_db)):
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
        token_data = schemas.TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = db.user.get_user_by_name(sess, token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), sess: Session = Depends(get_db)):
    user = db.user.authenticate_user(sess, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @app.post("/wg/update/", response_model=List[schemas.WireGuard])

@app.get("/api/wg/server/all", response_model=typing.List[schemas.WGServer])
def get_interfaces(sess: Session = Depends(get_db)):
    interfaces = db.wireguard.server_get_all(sess)
    for iface in interfaces:
        iface.is_running = script.wireguard.is_running(iface)

    return interfaces


@app.post("/api/wg/server/add", response_model=schemas.WGServer)
def add_interface(form_data: schemas.WGServer, sess: Session = Depends(get_db)):
    if form_data.interface is None or form_data.listen_port is None or form_data.address is None:
        raise HTTPException(status_code=400,
                            detail="Interface, Listen-Port and Address must be included in the schema.")

    try:
        wg_server = db.wireguard.server_add(sess, form_data)

        # Public/Private key
        private_key, public_key = script.wireguard.generate_keys()
        wg_server.private_key = private_key
        wg_server.public_key = public_key
        db.wireguard.server_key_pair_set(sess, wg_server)
        db.wireguard.server_generate_config(sess, wg_server)

        return wg_server
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/wg/server/edit", response_model=schemas.WGServer)
def edit_server(data: dict, sess: Session = Depends(get_db)):
    interface = data["interface"]
    server = schemas.WGServer(**data["server"])

    # Stop if running
    old = schemas.WGServer(interface=interface)

    if script.wireguard.is_running(old):
        script.wireguard.stop_interface(old)

    fields = set(old.__fields__) - {"peers", "is_running"}
    if not db.wireguard.server_update_field(sess, interface, server, fields):
        raise HTTPException(400, detail="Were not able to edit %s" % old.interface)

    script.wireguard.start_interface(server)

    return server


@app.get("/api/wg/generate_keypair", response_model=schemas.KeyPair)
def generate_key_pair():
    private_key, public_key = script.wireguard.generate_keys()
    return schemas.KeyPair(
        private_key=private_key,
        public_key=public_key
    )


@app.get("/api/wg/generate_psk", response_model=schemas.PSK)
def generate_psk():
    return schemas.PSK(
        psk=script.wireguard.generate_psk()
    )


@app.post("/api/wg/server/stop", response_model=schemas.WGServer)
def start_server(form_data: schemas.WGServer, ):
    script.wireguard.stop_interface(form_data)
    form_data.is_running = script.wireguard.is_running(form_data)
    return form_data


@app.post("/api/wg/server/start", response_model=schemas.WGServer)
def start_server(form_data: schemas.WGServer, sess: Session = Depends(get_db)):
    db.wireguard.server_generate_config(sess, form_data)
    script.wireguard.start_interface(form_data)
    form_data.is_running = script.wireguard.is_running(form_data)
    return form_data


@app.post("/api/wg/server/restart", response_model=schemas.WGServer)
def start_server(form_data: schemas.WGServer, sess: Session = Depends(get_db)):
    db.wireguard.server_generate_config(sess, form_data)
    script.wireguard.restart_interface(form_data)
    form_data.is_running = script.wireguard.is_running(form_data)
    return form_data


@app.post("/api/wg/server/delete", response_model=schemas.WGServer)
def delete_server(form_data: schemas.WGServer, sess: Session = Depends(get_db)):
    # Stop if running
    if script.wireguard.is_running(form_data):
        script.wireguard.stop_interface(form_data)

    if not db.wireguard.server_remove(sess, form_data):
        raise HTTPException(400, detail="Were not able to delete %s" % form_data.interface)
    return form_data


@app.post("/api/wg/server/peer/add", response_model=schemas.WGPeer)
def add_peer(form_data: schemas.WGServer, sess: Session = Depends(get_db)):
    wg_peer = schemas.WGPeer(server=form_data.interface)

    # Insert initial peer
    wg_peer = db.wireguard.peer_insert(sess, wg_peer)

    # If server is running. Add peer
    if script.wireguard.is_running(form_data):
        script.wireguard.add_peer(form_data, wg_peer)

    db.wireguard.peer_generate_config(sess, wg_peer)

    return wg_peer


@app.post("/api/wg/server/peer/delete", response_model=schemas.WGPeer)
def delete_peer(form_data: schemas.WGPeer, sess: Session = Depends(get_db)):
    if not db.wireguard.peer_remove(sess, form_data):
        raise HTTPException(400, detail="Were not able to delete peer %s (%s)" % (form_data.name, form_data.public_key))

    server = schemas.WGServer(interface=form_data.server)
    if script.wireguard.is_running(server):
        script.wireguard.remove_peer(server, form_data)

    return form_data


@app.post("/api/wg/server/peer/edit", response_model=schemas.WGPeer)
def edit_peer(form_data: schemas.WGPeer, sess: Session = Depends(get_db)):
    wg_peer = db.wireguard.peer_update(sess, form_data)
    db.wireguard.peer_generate_config(sess, wg_peer)

    return wg_peer


@app.post("/api/wg/server/stats")
def edit_peer(form_data: schemas.WGServer):
    stats = script.wireguard.get_stats(form_data)
    return JSONResponse(content=stats)


@app.post("/api/wg/server/peer/config", response_model=schemas.WGPeerConfig)
def config_peer(form_data: schemas.WGPeer, sess: Session = Depends(get_db)):
    db_peer = db.wireguard.peer_query_get_by_address(sess, form_data.address, form_data.server).one()

    with open(const.PEER_FILE(db_peer), "r") as f:
        conf_file = f.read()

    return schemas.WGPeerConfig(config=conf_file)


@app.post("/api/wg/server/config", response_model=schemas.WGPeerConfig)
def config_server(form_data: schemas.WGServer):
    with open(const.SERVER_FILE(form_data.interface), "r") as f:
        conf_file = f.read()

    return schemas.WGPeerConfig(config=conf_file)


@app.post("/api/users/create/")
def create_user(form_data: schemas.UserInDB, sess: Session = Depends(get_db)):
    user = db.user.get_user_by_name(sess, form_data.username)

    # User already exists
    if user:
        if not db.user.authenticate_user(sess, form_data.username, form_data.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

    else:

        # Create the user
        if not db.user.create_user(sess, models.User(
                username=form_data.username,
                password=form_data.password,
                full_name=form_data.full_name,
                email=form_data.email,
                role=form_data.role,
        )):
            raise HTTPException(status_code=400, detail="Could not create user")

    return login_for_access_token(OAuth2PasswordRequestForm(
        username=form_data.username,
        password=form_data.password,
        scope=""
    ), sess)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", include_in_schema=True)
def root():
    return FileResponse('build/index.html')


app.mount("/", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'build')), name="static")


# @app.get("/")
# async def read_root():
#    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":

    async def main():
        if not script.wireguard.is_installed():
            print("NOT INSTALLED!")
            exit(0)
        await database.connect()

        # TODO - GUI EVENT - Create new WG interface and post to backend
        wg_interface_in = dict(
            address="10.0.100.1/24",
            listen_port=5192,
            interface="wg0",
            endpoint=None,
            private_key=None,
            public_key=None,
            shared_key=None,
            post_up=None,
            post_down=None,
            peers=[]
        )

        wg_interface = schemas.WGServer(**wg_interface_in)

        sess = SessionLocal()

        if not db.wireguard.server_add(sess, wg_interface):
            print("Already exists. error")

        # Public/Private key
        private_key, public_key = script.wireguard.generate_keys()
        wg_interface.private_key = private_key
        wg_interface.public_key = public_key
        db.wireguard.server_key_pair_set(sess, wg_interface)

        # Shared key
        shared_key = script.wireguard.generate_psk()
        wg_interface.shared_key = shared_key
        db.wireguard.server_preshared_key(sess, wg_interface)

        # Post UP
        wg_interface.post_up = "echo 'LOL2'"
        db.wireguard.server_post_up_set(sess, wg_interface)

        # Post DOWN
        wg_interface.post_down = "echo 'LOL'"
        db.wireguard.server_post_down_set(sess, wg_interface)

        # Listen port
        wg_interface.listen_port = 5192
        if not db.wireguard.server_listen_port_set(sess, wg_interface):
            print("FAILED!")

        # Address
        wg_interface.address = "10.0.100.1/24"
        db.wireguard.server_ip_address_set(sess, wg_interface)

        # Endpoint
        wg_interface.endpoint = "10.0.0.135"
        db.wireguard.server_endpoint_set(sess, wg_interface)

        # TODO - Creates peer
        wg_peer_in = dict(
            server="wg0"
        )

        # CReate schema instance
        wg_peer = schemas.WGPeer(**wg_peer_in)

        # Insert initial peer
        wg_peer = db.wireguard.peer_insert(sess, wg_peer)
        print(wg_peer)

        # Set DNS of peer
        wg_peer.dns = ["sysx.no"]
        wg_peer = db.wireguard.peer_dns_set(sess, wg_peer)

        # Update priv_pub key
        wg_peer = db.wireguard.peer_key_pair_generate(sess, wg_peer)

        print(wg_peer)

        all_peers = db.wireguard.peer_get(sess, wg_interface)
        print(all_peers)

        db.wireguard.peer_generate_config(sess, wg_peer)
        print("-----")
        db_interface = db.wireguard.server_query_get_by_interface(sess, wg_interface.interface).one()
        db.wireguard.server_generate_config(sess, wg_interface.from_orm(db_interface))

        if script.wireguard.is_running(db_interface):
            script.wireguard.stop_interface(db_interface)
        script.wireguard.start_interface(db_interface)
        # script.wireguard.stop_interface(db_interface)

        if script.wireguard.is_running(db_interface):
            script.wireguard.add_peer(wg_interface, wg_peer)
            script.wireguard.remove_peer(wg_interface, wg_peer)

        db.wireguard.start_client(sess, wg_peer)


    # loop = asyncio.get_event_loop()
    # loop.create_task(main())
    # asyncio.get_event_loop().run_forever()

    uvicorn.run("__main__:app", reload=True)
