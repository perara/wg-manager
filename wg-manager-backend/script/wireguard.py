import logging
import random
import subprocess
import tempfile
import requests
import typing
import configparser

from sqlalchemy.orm import Session

import const
import schemas
import os
import re
import ipaddress
import util
from database import models
from database.database import SessionLocal

_LOGGER = logging.getLogger(__name__)


class WGAlreadyStartedError(Exception):
    pass


class WGAlreadyStoppedError(Exception):
    pass


class WGPermissionsError(Exception):
    pass


class WGPortAlreadyInUse(Exception):
    pass


class TempServerFile():
    def __init__(self, server: schemas.WGServer):
        self.server = server
        self.td = tempfile.TemporaryDirectory(prefix="wg_man_")
        self.server_file = os.path.join(self.td.name, f"{server.interface}.conf")

    def __enter__(self):
        with open(self.server_file, "w+") as f:
            f.write(self.server.configuration)
        return self.server_file

    def __exit__(self, type, value, traceback):
        self.td.cleanup()


def _run_wg(server: schemas.WGServer, command):
    try:
        output = subprocess.check_output(const.CMD_WG_COMMAND + command, stderr=subprocess.STDOUT)
        return output
    except Exception as e:
        if b'Operation not permitted' in e.output:
            raise WGPermissionsError("The user has insufficient permissions for interface %s" % server.interface)


def is_installed():
    output = subprocess.check_output(const.CMD_WG_COMMAND)
    return output == b'' or b'interface' in output


def generate_keys() -> typing.Dict[str, str]:
    private_key = subprocess.check_output(const.CMD_WG_COMMAND + ["genkey"])
    public_key = subprocess.check_output(
        const.CMD_WG_COMMAND + ["pubkey"],
        input=private_key
    )

    private_key = private_key.decode("utf-8").strip()
    public_key = public_key.decode("utf-8").strip()
    return dict(
        private_key=private_key,
        public_key=public_key
    )


def generate_psk():
    return subprocess.check_output(const.CMD_WG_COMMAND + ["genpsk"]).decode("utf-8").strip()


def start_interface(server: typing.Union[schemas.WGServer, schemas.WGPeer]):
    with TempServerFile(server) as server_file:
        try:
            # print(*const.CMD_WG_QUICK, "up", server_file)
            output = subprocess.check_output(const.CMD_WG_QUICK + ["up", server_file], stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            print(e.output)
            if b'already exists' in e.output:
                raise WGAlreadyStartedError("The wireguard device %s is already started." % server.interface)
            elif b'Address already in use' in e.output:
                raise WGPortAlreadyInUse("The port %s is already used by another application." % server.listen_port)


def stop_interface(server: schemas.WGServer):
    with TempServerFile(server) as server_file:
        try:
            output = subprocess.check_output(const.CMD_WG_QUICK + ["down", server_file], stderr=subprocess.STDOUT)
            return output
        except Exception as e:
            if b'is not a WireGuard interface' in e.output:
                raise WGAlreadyStoppedError("The wireguard device %s is already stopped." % server.interface)


def restart_interface(server: schemas.WGServer):
    try:
        stop_interface(server)
    except WGAlreadyStoppedError:
        pass
    start_interface(server)


def is_running(server: schemas.WGServer):
    try:
        output = _run_wg(server, ["show", server.interface])
        if output is None or b'Unable to access interface: No such device' in output:
            return False
    except Exception as e:
        print(e.output)
        if b'No such device' in e.output:
            return False
    return True


def add_peer(server: schemas.WGServer, peer: schemas.WGPeer):
    try:
        output = _run_wg(server, ["set", server.interface, "peer", peer.public_key, "allowed-ips", peer.address])
        return output == b''
    except Exception as e:
        _LOGGER.exception(e)
        return False


def remove_peer(server: schemas.WGServer, peer: schemas.WGPeer):
    try:
        output = _run_wg(server, ["set", server.interface, "peer", peer.public_key, "remove"])
        return output == b''
    except Exception as e:
        _LOGGER.exception(e)
        return False


def get_stats(server: schemas.WGServer):
    try:
        output = _run_wg(server, ["show", server.interface])
        if not output:
            return []
        regex = r"peer:.*?^\n"
        test_str = output.decode("utf-8") + "\n"

        peers = []

        peers_raw = re.findall(regex, test_str, re.MULTILINE | re.DOTALL)

        for peer in peers_raw:
            peer = peer.strip()
            lines = [x.split(": ")[1] for x in peer.split("\n")]

            if len(lines) == 2:
                public_key, allowed_ips = lines
                peers.append(dict(
                    public_key=public_key,
                    client_endpoint=None,
                    allowed_ips=allowed_ips,
                    handshake=None,
                    rx=None,
                    tx=None
                ))
            elif len(lines) == 5 or len(lines) == 6:
                public_key = lines[0]
                client_endpoint, allowed_ips, handshake, rx_tx = lines[-4:]  # [1] is sometimes psk

                rx = re.match(r"^(.*) received", rx_tx).group(1)
                tx = re.match(r"^.*, (.*)sent", rx_tx).group(1)
                peers.append(dict(
                    public_key=public_key,
                    client_endpoint=client_endpoint,
                    allowed_ips=allowed_ips,
                    handshake=handshake,
                    rx=rx,
                    tx=tx
                ))

            else:
                ValueError("We have not handled peers with line number of %s" % str(len(lines)))

        return peers
    except Exception as e:
        _LOGGER.exception(e)
        return []


def move_server_dir(interface, interface1):
    old_server_dir = const.SERVER_DIR(interface)
    old_server_file = const.SERVER_FILE(interface)
    new_server_dir = const.SERVER_DIR(interface1)
    new_server_file = old_server_file.replace(f"{interface}.conf", f"{interface1}.conf")

    os.rename(old_server_file, new_server_file)
    os.rename(old_server_dir, new_server_dir)


def generate_config(obj: typing.Union[typing.Dict[schemas.WGPeer, schemas.WGServer], schemas.WGServer]):
    if isinstance(obj, dict) and "server" in obj and "peer" in obj:
        template = "peer.j2"
        is_ipv6 = obj["server"].v6_address is not None
    elif isinstance(obj, schemas.WGServer) or isinstance(obj, models.WGServer):
        template = "server.j2"
        is_ipv6 = obj.v6_address is not None
    else:
        raise ValueError("Incorrect input type. Should be WGPeer or WGServer")

    result = util.jinja_env.get_template(template).render(
        data=obj,
        is_ipv6=is_ipv6
    )

    return result


def retrieve_client_conf_from_server(
        client_name,
        server_interface,
        server_host,
        server_api_key
):
    const.CLIENT_NAME = "client-1"
    const.CLIENT_SERVER_INTERFACE = "wg0"
    const.CLIENT_SERVER_HOST = "http://localhost:4200"
    const.CLIENT_API_KEY = "8bae20143fb962930614952d80634822361fd5ab9488053866a56de5881f9d7b"

    assert server_interface is not None and \
           server_host is not None and \
           server_api_key is not None, "Client configuration is invalid: %s, %s, api-key-is-null?: %s" % (
        server_interface,
        server_host,
        server_api_key is None
    )

    api_get_or_add = f"{server_host}/api/v1/peer/configuration/get_or_add"

    response = requests.post(api_get_or_add, json={
        "server_interface": server_interface,
        "name": client_name
    }, headers={
        "X-API-Key": server_api_key
    })

    if response.status_code != 200:
        print(response.text)
        raise RuntimeError("Could not retrieve config from server: %s" % (api_get_or_add,))

    return response.text


def create_client_config(sess: Session, configuration, client_name, client_routes):

    parser = configparser.ConfigParser()
    parser.read_string(configuration)
    public_key = parser["Peer"]["PublicKey"]

    assert len(set(parser.sections()) - {"Interface", "Peer"}) == 0, "Missing Interface or Peer section"

    # Parse Server
    # Check if server already exists.

    is_new_server = False
    is_new_peer = False

    try:
        db_server = sess.query(models.WGServer).filter_by(
            public_key=public_key,
            read_only=1
        ).one()
    except:
        db_server = None

    if db_server is None:
        db_server = models.WGServer()
        is_new_server = True

    db_server.read_only = 1
    db_server.public_key = parser["Peer"]["PublicKey"]
    db_server.address = parser["Peer"]["Endpoint"]
    db_server.listen_port = random.randint(69000, 19292009)

    db_server.v6_address = "N/A"
    db_server.v6_subnet = 0
    db_server.address = "N/A"
    db_server.subnet = 0
    db_server.private_key = "N/A"
    db_server.dns = "N/A"
    db_server.post_up = "N/A"
    db_server.post_down = "N/A"
    db_server.is_running = False
    db_server.configuration = "N/A"

    # Parse client
    try:
        db_peer = sess.query(models.WGPeer).filter_by(
            private_key=parser["Interface"]["PrivateKey"],
            read_only=1
        ).one()
    except:
        db_peer = None

    if db_peer is None:
        db_peer = models.WGPeer()
        is_new_peer = True

    db_peer.read_only = 1
    db_peer.name = client_name

    addresses_split = parser["Interface"]["Address"].split(",")
    assert len(addresses_split) > 0, "Must be at least one address"

    for address_with_subnet in addresses_split:
        addr, subnet = address_with_subnet.split("/")

        if isinstance(ipaddress.ip_address(addr), ipaddress.IPv4Address):
            db_peer.address = address_with_subnet
        elif isinstance(ipaddress.ip_address(addr), ipaddress.IPv6Address):
            db_peer.v6_address = address_with_subnet
        else:
            raise RuntimeError("Incorrect IP Address: %s, %s" % (addr, subnet))

    db_peer.private_key = parser["Interface"]["PrivateKey"]
    db_peer.public_key = "N/A"
    db_peer.allowed_ips = client_routes if client_routes else parser["Peer"]["AllowedIPs"]
    db_peer.configuration = configuration
    db_server.interface = f"client_{db_peer.name}"
    db_server.configuration = configuration
    try:
        db_peer.shared_key = parser["Interface"]["PrivateKey"]
    except KeyError:
        db_peer.shared_key = "N/A"

    db_peer.dns = parser["Interface"]["DNS"]
    db_peer.server = db_server

    if is_new_server:
        sess.add(db_server)
    else:
        sess.merge(db_server)
    sess.commit()

    if is_new_peer:
        sess.add(db_peer)
    else:
        sess.merge(db_peer)
    sess.commit()

    if const.CLIENT_START_AUTOMATICALLY and not is_running(db_server):
        start_interface(db_server)


def load_environment_clients(sess: Session):
    i = 1
    while True:

        client_name = os.getenv(f"CLIENT_{i}_NAME", None)
        client_server_interface = os.getenv(f"CLIENT_{i}_SERVER_INTERFACE", None)
        client_server_host = os.getenv(f"CLIENT_{i}_SERVER_HOST", None)
        client_api_key = os.getenv(f"CLIENT_{i}_API_KEY", None)
        client_routes = os.getenv(f"CLIENT_{i}_ROUTES", None)

        if client_api_key is None or \
                client_server_interface is None or \
                client_server_host is None or \
                client_api_key is None:
            break

        _LOGGER.warning(
            f"Found client configuration: name={client_name},siface={client_server_interface},shost={client_server_host}")

        config = retrieve_client_conf_from_server(
            client_name=client_name,
            server_interface=client_server_interface,
            server_host=client_server_host,
            server_api_key=client_api_key
        )

        create_client_config(sess, configuration=config, client_name=client_name, client_routes=client_routes)

        i += 1

if __name__ == "__main__":
    os.environ["CLIENT_1_NAME"] = "client-1"
    os.environ["CLIENT_1_SERVER_INTERFACE"] = "wg0"
    os.environ["CLIENT_1_SERVER_HOST"] = "http://localhost:4200"
    os.environ["CLIENT_1_API_KEY"] = "8bae20143fb962930614952d80634822361fd5ab9488053866a56de5881f9d7b"
    os.environ["CLIENT_2_NAME"] = "client-2"
    os.environ["CLIENT_2_SERVER_INTERFACE"] = "wg0"
    os.environ["CLIENT_2_SERVER_HOST"] = "http://localhost:4200"
    os.environ["CLIENT_2_API_KEY"] = "8bae20143fb962930614952d80634822361fd5ab9488053866a56de5881f9d7b"
    sess: Session = SessionLocal()
    load_environment_clients(sess)
    sess.close()


