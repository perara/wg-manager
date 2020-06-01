import os
import string
from database import SessionLocal
from sqlalchemy.orm import Session

import models
import script.wireguard

# Quit if there isn't any interface specified for autostart
if "AUTOSTART_INTERFACES" not in os.environ or not os.environ.get("AUTOSTART_INTERFACES"):
    quit()

interfaces = os.environ.get("AUTOSTART_INTERFACES").split(",")
_db: Session = SessionLocal()

for i in interfaces:
    try:
        i = i.strip()
        server = _db.query(models.WGServer).filter(models.WGServer.interface == i).first()
        if not server:
            raise Exception('Could not find the interface ' + i)

        last_state = server.is_running
        if script.wireguard.is_installed() and last_state and not script.wireguard.is_running(server):
            script.wireguard.start_interface(server)
            print('Automatically started the interface ' + i)
        elif last_state:
            print('The interface ' + i + ' is already started')

    except Exception as e:
        print(e)

_db.close()
