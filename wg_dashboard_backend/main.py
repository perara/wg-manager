import logging
import os

import typing
from sqlalchemy_utils import database_exists
from starlette.middleware.base import BaseHTTPMiddleware

import middleware
from database import engine, SessionLocal
from routers.v1 import user, server, peer, wg
import script.wireguard
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
from const import DATABASE_URL
from migrate import DatabaseAlreadyControlledError
from migrate.versioning.shell import main
import models


app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=middleware.db_session_middleware)

_db: Session = SessionLocal()

# Ensure database existence
if not database_exists(engine.url):
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    if not ADMIN_USERNAME:
        raise RuntimeError("Database does not exist and no ADMIN_USER is set")

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    if not ADMIN_PASSWORD:
        raise RuntimeError("Database does not exist and no ADMIN_PASSWORD is set")

    # Create database from metadata
    models.Base.metadata.create_all(engine)

    # Create default user
    _db.add(models.User(
        username=ADMIN_USERNAME,
        password=middleware.get_password_hash(ADMIN_PASSWORD),
        full_name="Admin",
        role="admin",
        email=""
    ))
_db.commit()


# Do migrations
try:
    main(["version_control", DATABASE_URL, "migrations"])
except DatabaseAlreadyControlledError:
    pass
main(["upgrade", DATABASE_URL, "migrations"])


servers: typing.List[models.WGServer] = _db.query(models.WGServer).all()
for s in servers:
    try:
        last_state = s.is_running
        if script.wireguard.is_installed() and last_state and not script.wireguard.is_running(s):
            script.wireguard.start_interface(s)
    except Exception as e:
        print(e)

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
    uvicorn.run("__main__:app", reload=True)
