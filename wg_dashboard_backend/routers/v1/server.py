import tempfile
from os.path import exists

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import const
import models
import schemas
import middleware
import db.wireguard
import script.wireguard
import typing

router = APIRouter()


@router.get("/all", response_model=typing.List[schemas.WGServer])
def servers_all(
        sess: Session = Depends(middleware.get_db)
):
    interfaces = db.wireguard.server_get_all(sess)
    for iface in interfaces:
        iface.is_running = script.wireguard.is_running(iface)

    return interfaces


@router.post("/add", response_model=schemas.WGServer)
def add_interface(
        server: schemas.WGServerAdd,
        sess: Session = Depends(middleware.get_db)
):
    server.post_up = server.post_up if server.post_up != "" else const.DEFAULT_POST_UP
    server.post_down = server.post_up if server.post_up != "" else const.DEFAULT_POST_DOWN
    peers = server.peers if server.peers else []

    # Public/Private key
    try:

        if server.filter_query(sess).count() != 0:
            raise HTTPException(status_code=400, detail="The server interface %s already exists in the database" % server.interface)

        if not server.private_key:
            keys = script.wireguard.generate_keys()
            server.private_key = keys["private_key"]
            server.public_key = keys["public_key"]

        server.configuration = script.wireguard.generate_config(server)
        server.peers = []
        server.sync(sess)

        if len(peers) > 0:
            server.from_db(sess)

            for schemaPeer in peers:
                schemaPeer.server_id = server.id
                schemaPeer.configuration = script.wireguard.generate_config(dict(
                    peer=schemaPeer,
                    server=server
                ))
                dbPeer = models.WGPeer(**schemaPeer.dict())
                sess.add(dbPeer)
                sess.commit()

        server.from_db(sess)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return server


@router.post("/stop", response_model=schemas.WGServer)
def stop_server(
        server: schemas.WGServer,
        sess: Session = Depends(middleware.get_db)
):
    script.wireguard.stop_interface(server)
    server.is_running = script.wireguard.is_running(server)
    server.sync(sess)
    return server


@router.post("/start", response_model=schemas.WGServer)
def start_server(
        server: schemas.WGServer,
        sess: Session = Depends(middleware.get_db)
):
    script.wireguard.start_interface(server)
    server.is_running = script.wireguard.is_running(server)
    server.sync(sess)
    return server


@router.post("/restart", response_model=schemas.WGServer)
def restart_server(
        server: schemas.WGServer,
        sess: Session = Depends(middleware.get_db)
):
    script.wireguard.restart_interface(server)
    server.is_running = script.wireguard.is_running(server)
    server.sync(sess)

    return server


@router.post("/delete", response_model=schemas.WGServer)
def delete_server(
        form_data: schemas.WGServer,
        sess: Session = Depends(middleware.get_db)
):
    # Stop if running
    if script.wireguard.is_running(form_data):
        script.wireguard.stop_interface(form_data)

    if not db.wireguard.server_remove(sess, form_data):
        raise HTTPException(400, detail="Were not able to delete %s" % form_data.interface)
    return form_data


@router.post("/stats", dependencies=[Depends(middleware.auth)])
def stats_server(server: schemas.WGServer):
    stats = script.wireguard.get_stats(server)
    return JSONResponse(content=stats)


@router.post("/edit", response_model=schemas.WGServer)
def edit_server(
        data: dict, sess: Session = Depends(middleware.get_db)
):
    interface = data["interface"]
    old = schemas.WGServer(interface=interface).from_db(sess)

    # Stop if running
    if script.wireguard.is_running(old):
        script.wireguard.stop_interface(old)

    # Update server
    server = schemas.WGServer(**data["server"])
    server.configuration = script.wireguard.generate_config(server)
    server = old.update(sess, new=server)

    # Update peers
    for peer_data in server.peers:
        peer = schemas.WGPeer(**peer_data)
        peer.configuration = script.wireguard.generate_config(dict(
            peer=peer,
            server=server
        ))
        peer.sync(sess)

    script.wireguard.start_interface(server)
    server.is_running = script.wireguard.is_running(server)
    server.sync(sess)
    server.from_db(sess)

    return server

