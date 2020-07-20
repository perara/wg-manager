from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from zipfile import ZipFile
from io import BytesIO
import middleware
from starlette.responses import StreamingResponse
import schemas
import script.wireguard
import db.wireguard

router = APIRouter()


@router.get("/generate_psk", response_model=schemas.PSK)
def generate_psk():
    return schemas.PSK(
        psk=script.wireguard.generate_psk()
    )


@router.get("/generate_keypair", response_model=schemas.KeyPair)
def generate_key_pair():
    keys = script.wireguard.generate_keys()
    private_key = keys["private_key"]
    public_key = keys["public_key"]
    return schemas.KeyPair(
        private_key=private_key,
        public_key=public_key
    )


@router.get("/dump")
def dump_database(
        sess: Session = Depends(middleware.get_db)
):
    in_memory = BytesIO()
    zf = ZipFile(in_memory, mode="w")
    for server in db.wireguard.server_get_all(sess):
        zf.writestr(f"{server.interface}/{server.interface}.conf", server.configuration)

        for peer in server.peers:
            zf.writestr(f"{server.interface}/peers/{peer.name}_{peer.address.replace('.','-')}.conf", server.configuration)

    zf.close()
    in_memory.seek(0)

    now = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    return StreamingResponse(in_memory, media_type="application/zip", headers={
        "Content-Disposition": f'attachment; filename="wg-manager-dump-{now}.zip"'
    })
