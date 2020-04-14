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
    uvicorn.run("__main__:app", reload=True)
