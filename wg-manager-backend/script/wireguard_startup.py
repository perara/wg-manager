import os
import typing

from sqlalchemy.orm import Session

import const
from database import models
from database.database import SessionLocal
from db.api_key import add_initial_api_key_for_admin
from db.wireguard import server_add_on_init
from script.wireguard import is_installed, start_interface, is_running, load_environment_clients


def setup_on_start():
    _db: Session = SessionLocal()
    servers: typing.List[models.WGServer] = _db.query(models.WGServer).all()
    for s in servers:
        try:
            last_state = s.is_running
            if is_installed() and last_state and is_running(s):
                start_interface(s)
        except Exception as e:
            print(e)

    if const.CLIENT:
        load_environment_clients(_db)

    if const.SERVER_INIT_INTERFACE is not None:
        server_add_on_init(_db)

    if const.SERVER_STARTUP_API_KEY is not None:
        ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
        add_initial_api_key_for_admin(_db, const.SERVER_STARTUP_API_KEY, ADMIN_USERNAME)
    _db.close()
