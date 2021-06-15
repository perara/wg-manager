import ipaddress
import json
import os
import shutil
import typing

from starlette.exceptions import HTTPException

import const
import script.wireguard
from sqlalchemy.orm import Session
from database import models
import schemas
from loguru import logger

from util import WGMHTTPException


def start_client(sess: Session, peer: schemas.WGPeer):
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    client_file = os.path.join(const.CLIENT_DIR(db_peer.server.interface), str(db_peer.id) + ".conf")
    import subprocess
    output = subprocess.check_output(const.CMD_WG_QUICK + ["up", client_file], stderr=subprocess.STDOUT)


def get_server_by_id(sess: Session, server_id):
    return sess.query(models.WGServer).filter_by(id=server_id).one()


def peer_query_get_by_address(sess: Session, address: str, server: str):
    return sess.query(models.WGPeer) \
        .filter(models.WGPeer.address == address) \
        .filter(models.WGPeer.server == server)


def peer_dns_set(sess: Session, peer: schemas.WGPeer) -> schemas.WGPeer:
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    db_peer.dns = peer.dns

    sess.add(db_peer)
    sess.commit()

    return peer.from_orm(db_peer)


def peer_remove(sess: Session, peer: schemas.WGPeer) -> bool:
    db_peers = sess.query(models.WGPeer).filter_by(id=peer.id).all()

    for db_peer in db_peers:
        sess.delete(db_peer)
        sess.commit()

    server_update_configuration(sess, peer.server_id)

    return True


def peer_edit(sess: Session, peer: schemas.WGPeer):
    # Retrieve server from db
    server: models.WGServer = get_server_by_id(sess, peer.server_id)

    # Generate peer configuration
    peer.configuration = script.wireguard.generate_config(dict(
        peer=peer,
        server=server
    ))

    # Update database record for Peer
    sess.query(models.WGPeer) \
        .filter_by(id=peer.id) \
        .update(peer.dict(exclude={"id"}))
    sess.commit()

    server_update_configuration(sess, server.id)

    return peer


def peer_key_pair_generate(sess: Session, peer: schemas.WGPeer) -> schemas.WGPeer:
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    private_key, public_key = script.wireguard.generate_keys()
    db_peer.private_key = private_key
    db_peer.public_key = public_key

    sess.add(db_peer)
    sess.commit()

    return peer.from_orm(db_peer)


def peer_ip_address_set(sess: Session, peer: schemas.WGPeer) -> schemas.WGPeer:
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    db_peer.address = peer.address
    sess.add(db_peer)
    sess.commit()
    return peer.from_orm(db_peer)


def peer_update(sess: Session, peer: schemas.WGPeer) -> schemas.WGPeer:
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    db_peer.address = peer.address
    db_peer.public_key = peer.public_key
    db_peer.private_key = peer.private_key
    db_peer.name = peer.name
    db_peer.dns = peer.dns
    db_peer.allowed_ips = peer.allowed_ips

    sess.add(db_peer)
    sess.commit()

    return peer.from_orm(db_peer)


def peer_get(sess: Session, server: schemas.WGServer) -> typing.List[schemas.WGPeer]:
    db_server = server_query_get_by_interface(sess, server.interface).one()
    return db_server.peers


def server_query_get_by_interface(sess: Session, interface: str):
    return sess.query(models.WGServer) \
        .filter(models.WGServer.interface == interface)


def server_update_field(sess: Session, interface: str, server: schemas.WGServer, fields: typing.Set):
    if server_query_get_by_interface(sess, interface) \
            .update(
        server.dict(include=fields), synchronize_session=False
    ) == 1:
        sess.commit()
        return True
    return False


def server_get_all(sess: Session) -> typing.List[schemas.WGServer]:
    db_interfaces = sess.query(models.WGServer) \
        .all()
    return [schemas.WGServer.from_orm(db_interface) for db_interface in db_interfaces]


def server_add_on_init(sess: Session):
    """
    Routine for adding server from env variable.
    :param server:
    :param sess:
    :return:
    """
    try:
        init_data = json.loads(const.SERVER_INIT_INTERFACE)

        if init_data["endpoint"] == "||external||":
            import requests
            init_data["endpoint"] = requests.get("https://api.ipify.org").text
        elif init_data["endpoint"] == "||internal||":
            import socket
            init_data["endpoint"] = socket.gethostbyname(socket.gethostname())

        if sess.query(models.WGServer) \
                .filter_by(endpoint=init_data["endpoint"], listen_port=init_data["listen_port"]) \
                .count() == 0:
            # Only add if it does not already exists.
            server_add(schemas.WGServerAdd(**init_data), sess, start=const.SERVER_INIT_INTERFACE_START)
    except Exception as e:
        logger.warning("Failed to setup initial server interface with exception:")
        logger.exception(e)


def server_add(server: schemas.WGServerAdd, sess: Session, start=False):
    # Configure POST UP with defaults if not manually set.
    if server.post_up == "":
        server.post_up = const.DEFAULT_POST_UP
        if server.v6_address is not None:
            server.post_up += const.DEFAULT_POST_UP_v6

    # Configure POST DOWN with defaults if not manually set.
    if server.post_down == "":
        server.post_down = const.DEFAULT_POST_DOWN
        if server.v6_address is not None:
            server.post_down += const.DEFAULT_POST_DOWN_v6

    peers = server.peers if server.peers else []

    all_interfaces = sess.query(models.WGServer).all()
    check_interface_exists = any(map(lambda el: el.interface == server.interface, all_interfaces))
    check_v4_address_exists = any(map(lambda el: el.address == server.address, all_interfaces))
    check_v6_address_exists = any(map(lambda el: el.v6_address == server.v6_address, all_interfaces))
    check_listen_port_exists = any(map(lambda el: str(el.listen_port) == str(server.listen_port), all_interfaces))
    if check_interface_exists:
        raise WGMHTTPException(
            status_code=400,
            detail=f"There is already a interface with the name: {server.interface}")

    if check_v4_address_exists:
        raise WGMHTTPException(
            status_code=400,
            detail=f"There is already a interface with the IPv4 address: {server.address}")

    if server.v6_support and check_v6_address_exists:
        raise WGMHTTPException(
            status_code=400,
            detail=f"There is already a interface with the IPv6 address: {server.v6_address}")

    if check_listen_port_exists:
        raise WGMHTTPException(
            status_code=400,
            detail=f"There is already a interface listening on port: {server.listen_port}")

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

    if start and not script.wireguard.is_running(server):
        script.wireguard.start_interface(server)

    return server


def server_remove(sess: Session, server: schemas.WGServer) -> bool:
    db_server = server_query_get_by_interface(sess, server.interface).one()
    if db_server is None:
        raise ValueError("The server with interface %s is already deleted." % server.interface)

    sess.delete(db_server)
    sess.commit()

    shutil.rmtree(const.SERVER_DIR(db_server.interface))

    return True


def server_preshared_key(sess: Session, server: schemas.WGServer) -> bool:
    return server_update_field(sess, server.interface, server, {"shared_key"})


def server_key_pair_set(sess: Session, server: schemas.WGServer) -> bool:
    return server_update_field(sess, server.interface, server, {"private_key", "public_key"})


def server_listen_port_set(sess: Session, server: schemas.WGServer) -> bool:
    if server.listen_port < 1024 or server.listen_port > 65535:
        raise ValueError("The listen_port is not in port range 1024 < x < 65535")

    return server_update_field(sess, server.interface, server, {"listen_port"})


def server_ip_address_set(sess: Session, server: schemas.WGServer) -> bool:
    network = ipaddress.ip_network(server.address, False)
    if not network.is_private:
        raise ValueError("The network is not in private range")

    return server_update_field(sess, server.interface, server, {"address"})


def server_post_up_set(sess: Session, server: schemas.WGServer) -> bool:
    return server_update_field(sess, server.interface, server, {"post_up"})


def server_post_down_set(sess: Session, server: schemas.WGServer) -> bool:
    return server_update_field(sess, server.interface, server, {"post_down"})


def server_endpoint_set(sess: Session, server: schemas.WGServer) -> bool:
    return server_update_field(sess, server.interface, server, {"endpoint"})


def server_update_configuration(sess: Session, server_id: int) -> bool:
    # Generate server configuration
    server: models.WGServer = sess.query(models.WGServer).filter_by(id=server_id).one()
    server.configuration = script.wireguard.generate_config(server)
    sess.add(server)
    sess.commit()
