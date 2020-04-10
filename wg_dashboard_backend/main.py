import logging
import os
from sqlalchemy_utils import database_exists
from starlette.middleware.base import BaseHTTPMiddleware

import middleware
from database import engine, SessionLocal
from routers.v1 import user, server, peer, wg

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
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from fastapi import Depends, FastAPI

import models


app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=middleware.db_session_middleware)

if not database_exists(engine.url):
    models.Base.metadata.create_all(engine)
    # Create default user
    _db: Session = SessionLocal()
    _db.add(models.User(
        username=os.getenv("ADMIN_USERNAME", "admin"),
        password=middleware.get_password_hash(os.getenv("ADMIN_PASSWORD", "admin")),
        full_name="Admin",
        role="admin",
        email=""
    ))
    _db.commit()
    _db.close()


app.include_router(
    user.router,
    prefix="/api/v1",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}}
)


app.include_router(
    server.router,
    prefix="/api/v1/server",
    tags=["server"],
    dependencies=[Depends(middleware.auth)],
    responses={404: {"description": "Not found"}}
)


app.include_router(
    peer.router,
    prefix="/api/v1/peer",
    tags=["peer"],
    dependencies=[Depends(middleware.auth)],
    responses={404: {"description": "Not found"}}
)


app.include_router(
    wg.router,
    prefix="/api/v1/wg",
    tags=["wg"],
    dependencies=[Depends(middleware.auth)],
    responses={404: {"description": "Not found"}}
)


@app.get("/", include_in_schema=True)
def root():
    return FileResponse('build/index.html')


app.mount("/", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'build')), name="static")





@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass



if __name__ == "__main__":

    """async def main():
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

        db.wireguard.start_client(sess, wg_peer)"""

    uvicorn.run("__main__:app", reload=True)
