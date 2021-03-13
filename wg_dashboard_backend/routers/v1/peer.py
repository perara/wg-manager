import ipaddress
import itertools
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse

from database import models
import schemas
import middleware
import db.wireguard
import script.wireguard

router = APIRouter()


def generate_ip_address(server: schemas.WGServer, v6):
    if v6:
        address_space = set(
            itertools.islice(ipaddress.ip_network("fd42:42:42::1/64", strict=False).hosts(), 1, 1024)
        )
    else:
        address_space = set(ipaddress.ip_network(f"{server.address}/{server.subnet}", strict=False).hosts())
    occupied_space = set()

    # Try add server IP to list.
    try:
        occupied_space.add(ipaddress.ip_address(server.v6_address if v6 else server.address))
    except ValueError:
        pass

    for p in server.peers:

        # Try add peer ip to list.
        try:
            occupied_space.add(ipaddress.ip_address(p.v6_address if v6 else p.address))
        except ValueError as e:
            pass  # Ignore invalid addresses. These are out of address_space

    address_space -= occupied_space

    # Select first available address
    return str(list(sorted(address_space)).pop(0))


@router.post("/add", response_model=schemas.WGPeer)
def add_peer(
        peer_add: schemas.WGPeerConfigAdd,
        sess: Session = Depends(middleware.get_db)
):
    server = schemas.WGServer(interface=peer_add.server_interface).from_db(sess)

    if server is None:
        raise HTTPException(500, detail="The server-interface '%s' does not exist!" % peer_add.server_interface)

    peer = schemas.WGPeer(server_id=server.id)

    if server.v6_address:
        peer.v6_address = generate_ip_address(server, v6=True)
    peer.address = generate_ip_address(server, v6=False)

    # Private public key generation
    keys = script.wireguard.generate_keys()
    peer.private_key = keys["private_key"]
    peer.public_key = keys["public_key"]

    peer.allowed_ips = server.allowed_ips
    peer.keep_alive = server.keep_alive

    # Set unnamed
    peer.name = "Unnamed" if not peer_add.name else peer_add.name

    peer.dns = server.dns

    peer.configuration = script.wireguard.generate_config(dict(
        peer=peer,
        server=server
    ))

    db_peer = models.WGPeer(**peer.dict())
    sess.add(db_peer)
    sess.commit()

    # If server is running. Add peer
    if script.wireguard.is_running(server):
        script.wireguard.add_peer(server, peer)

    # Update server configuration
    db.wireguard.server_update_configuration(sess, db_peer.server_id)

    return schemas.WGPeer.from_orm(db_peer)


@router.post("/configuration/get_or_add")
def get_or_add_peer_return_config(peer_get: schemas.WGPeerConfigGetByName,
                        sess: Session = Depends(middleware.get_db)
                        ):
    server = sess.query(models.WGServer).filter_by(interface=peer_get.server_interface).one()
    peer = sess.query(models.WGPeer).filter_by(name=peer_get.name, server_id=server.id).all()

    if not peer:
        return add_peer_get_config(schemas.WGPeerConfigAdd(
            name=peer_get.name,
            server_interface=peer_get.server_interface
        ), sess=sess)

    peer = peer[0]

    return PlainTextResponse(peer.configuration)


@router.post("/configuration/add")
def add_peer_get_config(peer_add: schemas.WGPeerConfigAdd,
                        sess: Session = Depends(middleware.get_db)
                        ):
    wg_peer: schemas.WGPeer = add_peer(peer_add, sess)

    return PlainTextResponse(wg_peer.configuration)


@router.post("/delete", response_model=schemas.WGPeer)
def delete_peer(
        peer: schemas.WGPeer,
        sess: Session = Depends(middleware.get_db)
):

    server = sess.query(models.WGServer).filter_by(id=peer.server_id).one()

    if not db.wireguard.peer_remove(sess, peer):
        raise HTTPException(400, detail="Were not able to delete peer %s (%s)" % (peer.name, peer.public_key))

    if script.wireguard.is_running(schemas.WGServer(interface=server.interface)):
        script.wireguard.remove_peer(server, peer)

    return peer


@router.post("/edit")
def edit_peer(
        peer: schemas.WGPeer,
        sess: Session = Depends(middleware.get_db)
):

    peer = db.wireguard.peer_edit(sess, peer)

    return peer
