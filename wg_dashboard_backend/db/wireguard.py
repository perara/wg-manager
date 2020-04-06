import ipaddress
import os
import shutil
import typing
import const
import script.wireguard
from sqlalchemy import exists
from sqlalchemy.orm import Session
import util
import models
import schemas
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


def start_client(sess: Session, peer: schemas.WGPeer):
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    client_file = os.path.join(const.CLIENT_DIR(db_peer.server_ref.interface), str(db_peer.id) + ".conf")
    import subprocess
    output = subprocess.check_output(const.CMD_WG_QUICK + ["up", client_file], stderr=subprocess.STDOUT)
    print(output)


def server_generate_config(sess: Session, server: schemas.WGServer):
    db_server: models.WGServer = server_query_get_by_interface(sess, server.interface).one()

    result = util.jinja_env.get_template("server.j2").render(
        data=db_server
    )

    interface = db_server.interface
    server_file = const.SERVER_FILE(interface)

    with open(server_file, "w+") as f:
        f.write(result)
    os.chmod(server_file, 0o600)

    return result


def peer_generate_config(sess: Session, peer: schemas.WGPeer):
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()

    result = util.jinja_env.get_template("peer.j2").render(
        data=db_peer
    )

    peer_file = const.PEER_FILE(db_peer)

    with open(peer_file, "w+") as f:
        f.write(result)
    os.chmod(peer_file, 0o600)

    return result


def peer_query_get_by_address(sess: Session, address: str, server: str):
    return sess.query(models.WGPeer) \
        .filter(models.WGPeer.address == address) \
        .filter(models.WGPeer.server == server)


def peer_insert(sess: Session, peer: schemas.WGPeer) -> schemas.WGPeer:
    db_server: models.WGServer = server_query_get_by_interface(sess, peer.server).one()
    db_peer = models.WGPeer(**peer.dict())
    address_space = set(ipaddress.ip_network(db_server.address, strict=False).hosts())
    occupied_space = set()
    for p in db_server.peers:
        try:
            occupied_space.add(ipaddress.ip_address(p.address.split("/")[0]))
        except ValueError as e:
            print(e)
            pass  # Ignore invalid addresses. These are out of address_space

    address_space -= occupied_space

    # Select first available address
    db_peer.address = str(list(address_space).pop(0)) + "/32"

    # Private public key generation
    private_key, public_key = script.wireguard.generate_keys()
    db_peer.private_key = private_key
    db_peer.public_key = public_key

    # Set 0.0.0.0/0, ::/0 as default allowed ips
    db_peer.allowed_ips = ', '.join(const.PEER_DEFAULT_ALLOWED_IPS)

    # Set unnamed
    db_peer.name = "Unnamed"

    db_peer.dns = db_server.endpoint

    sess.add(db_peer)
    sess.commit()

    return peer.from_orm(db_peer)


def peer_dns_set(sess: Session, peer: schemas.WGPeer) -> schemas.WGPeer:
    db_peer: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).one()
    db_peer.dns = peer.dns

    sess.add(db_peer)
    sess.commit()

    return peer.from_orm(db_peer)


def peer_remove(sess: Session, peer: schemas.WGPeer) -> bool:
    db_peers: models.WGPeer = peer_query_get_by_address(sess, peer.address, peer.server).all()
    for db_peer in db_peers:
        sess.delete(db_peer)
        sess.commit()
        try:
            os.remove(const.PEER_FILE(db_peer))
        except:
            pass

    return True


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
    db_interfaces = sess.query(models.WGServer).all()
    return [schemas.WGServer.from_orm(db_interface) for db_interface in db_interfaces]


def server_add(sess: Session, server: schemas.WGServer) -> schemas.WGServer:
    if sess.query(exists().where(models.WGServer.interface == server.interface)).scalar():
        raise ValueError("The server interface %s already exists in the database" % server.interface)

    db_server = server.convert()
    sess.add(db_server)
    sess.commit()

    return server.from_orm(db_server)


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
