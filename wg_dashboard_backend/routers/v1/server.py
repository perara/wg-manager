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

    return db.wireguard.server_add(server, sess)


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
    if script.wireguard.is_running(server):
        stats = script.wireguard.get_stats(server)
    else:
        stats = []

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

        db_peer = models.WGPeer(**peer.dict())
        sess.merge(db_peer)
        sess.commit()

    script.wireguard.start_interface(server)
    server.is_running = script.wireguard.is_running(server)
    server.sync(sess)  # TODO - fix this sync mess.
    server.from_db(sess)

    return server


@router.get("/config/{server_id}", response_model=str)
def server_config(
        server_id: int,
        sess: Session = Depends(middleware.get_db)
):

    return db.wireguard.get_server_by_id(sess, server_id=server_id).configuration
