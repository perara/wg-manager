import os
import random
import string
IS_DOCKER = os.getenv("IS_DOCKER", "False") == "True"
DATABASE_FILE = "/config/database.db" if IS_DOCKER else "./database.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

OBFUSCATE_ENABLED = os.getenv("OBFUSCATION", "True") == "True"  # TODO should be false by default
OBFUSCATE_MODE = os.getenv("OBFUSCATION_MODE", "obfs4")
OBFUSCATE_SOCKS_TOR_PORT = int(os.getenv("OBFUSCATE_SOCKS_TOR_PORT", "5555"))
OBFUSCATE_TOR_LISTEN_ADDR = int(os.getenv("OBFUSCATE_TOR_LISTEN_ADDR", "5556"))
OBFUSCATE_SUPPORTED = ["obfs4"]
assert OBFUSCATE_MODE in OBFUSCATE_SUPPORTED, "Invalid OBFUSCATE_MODE=%s, Valid options are: %s" % (OBFUSCATE_MODE,
                                                                                                    OBFUSCATE_SUPPORTED)

os.makedirs("build", exist_ok=True)
DEFAULT_POST_UP = os.getenv("POST_UP", "iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE;")
DEFAULT_POST_DOWN = os.getenv("POST_DOWN", "iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE;")
DEFAULT_POST_UP_v6 = os.getenv("POST_UP_V6", "ip6tables -A FORWARD -i %i -j ACCEPT; ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE;")
DEFAULT_POST_DOWN_v6 = os.getenv("POST_DOWN_V6", "ip6tables -D FORWARD -i %i -j ACCEPT; ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE;")

SECRET_KEY = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
ALGORITHM = "HS256"

API_KEY_LENGTH = 32
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CMD_WG_COMMAND = ["wg"]
CMD_WG_QUICK = ["wg-quick"]

INIT_SLEEP = int(os.getenv("INIT_SLEEP", "0"))
SERVER_STARTUP_API_KEY = os.getenv("SERVER_STARTUP_API_KEY", None)
SERVER_INIT_INTERFACE = os.getenv("SERVER_INIT_INTERFACE", None)
SERVER_INIT_INTERFACE_START = os.getenv("SERVER_INIT_INTERFACE_START", "1") == "1"
SERVER = os.getenv("SERVER", "1") == "1"
CLIENT = os.getenv("CLIENT", "0") == "1"
CLIENT_START_AUTOMATICALLY = os.getenv("CLIENT_START_AUTOMATICALLY", "1") == "1"

AUTH_LOCAL_ENABLED = os.getenv("AUTH_LOCAL_ENABLED", "1") == "1"
AUTH_LDAP_ENABLED = os.getenv("AUTH_LDAP_ENABLED", "0") == "1"
AUTH_LDAP_SERVER = os.getenv("AUTH_LDAP_SERVER", None)
AUTH_LDAP_PORT = os.getenv("AUTH_LDAP_PORT", None)
AUTH_LDAP_USER = os.getenv("AUTH_LDAP_USER", None)
AUTH_LDAP_PASSWORD = os.getenv("AUTH_LDAP_PASSWORD", None)
AUTH_LDAP_BASE = os.getenv("AUTH_LDAP_BASE", None)
AUTH_LDAP_FILTER = os.getenv("AUTH_LDAP_FILTER", None)
AUTH_LDAP_ACTIVEDIRECTORY = os.getenv("AUTH_LDAP_ACTIVEDIRECTORY", "0") == "1"
AUTH_LDAP_DOMAIN = os.getenv("AUTH_LDAP_DOMAIN", None)
AUTH_LDAP_SECURITY = os.getenv("AUTH_LDAP_SECURITY", None)
AUTH_LDAP_SECURITY_VALID_CERTIFICATE = os.getenv("AUTH_LDAP_SECURITY_VALID_CERTIFICATE", "1") == "1"

assert AUTH_LOCAL_ENABLED or AUTH_LDAP_ENABLED, "At least one authentication engine must be enabled"

if AUTH_LDAP_ENABLED:
    assert AUTH_LDAP_SERVER, "AUTH_LDAP_SERVER is required"
    assert AUTH_LDAP_SECURITY in (None, "SSL", "TLS"), "Invalid value for AUTH_LDAP_SECURITY. Valid values are SSL and TLS"
    assert AUTH_LDAP_BASE, "AUTH_LDAP_BASE is required"
    assert AUTH_LDAP_FILTER, "AUTH_LDAP_FILTER is required"
    if AUTH_LDAP_ACTIVEDIRECTORY:
        assert AUTH_LDAP_DOMAIN, "AUTH_LDAP_DOMAIN is required when using Active Directory"
    if not AUTH_LDAP_PORT:
        if AUTH_LDAP_SECURITY == "SSL":
            AUTH_LDAP_PORT = 636
        else:
            AUTH_LDAP_PORT = 389
    else:
        AUTH_LDAP_PORT = int(AUTH_LDAP_PORT)

if not IS_DOCKER:
    CMD_WG_COMMAND = ["sudo"] + CMD_WG_COMMAND
    CMD_WG_QUICK = ["sudo"] + CMD_WG_QUICK
    DEFAULT_CONFIG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config")
else:
    DEFAULT_CONFIG_DIR = "/config"
    os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)


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
