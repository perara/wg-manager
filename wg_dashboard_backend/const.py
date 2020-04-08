import os
import random
import string
IS_DOCKER = os.getenv("IS_DOCKER", "False") == "True"
DATABASE_FILE = "/config/database.db" if IS_DOCKER else "./database.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

os.makedirs("build", exist_ok=True)

DEFAULT_POST_UP = os.getenv("POST_UP", "iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
DEFAULT_POST_DOWN = os.getenv("POST_DOWN", "iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE")

SECRET_KEY = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
CMD_WG_COMMAND = ["wg"]
CMD_WG_QUICK = ["wg-quick"]

if not IS_DOCKER:
    CMD_WG_COMMAND = ["sudo"] + CMD_WG_COMMAND
    CMD_WG_QUICK = ["sudo"] + CMD_WG_QUICK
    DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config")
else:
    DEFAULT_CONFIG_DIR = "/config"
    os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)

PEER_DEFAULT_ALLOWED_IPS = ["0.0.0.0/0", "::/0"]


ENV_CONFIG_DIR = os.getenv("ENV_CONFIG_DIR", DEFAULT_CONFIG_DIR)
os.makedirs(ENV_CONFIG_DIR, exist_ok=True)


def _server_dir(interface):
    s_dir = os.path.join(ENV_CONFIG_DIR, "server", interface)
    os.makedirs(s_dir, exist_ok=True)
    return s_dir


SERVER_DIR = _server_dir


def _client_dir(interface):
    c_dir = os.path.join(ENV_CONFIG_DIR, "server", interface, "clients")
    os.makedirs(c_dir, exist_ok=True)
    return c_dir


CLIENT_DIR = _client_dir

PEER_FILE = lambda db_peer: os.path.join(CLIENT_DIR(db_peer.server_ref.interface), str(db_peer.id) + ".conf")

SERVER_FILE = lambda interface: os.path.join(SERVER_DIR(interface), interface + ".conf")
