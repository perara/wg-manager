# wg-manager
The wg-manager provides an easy-to-use graphical web interface to import, setup, and manage WireGuard server(s).
[See Here](https://github.com/perara/wg-manager#Showcase)

The features of wg-manager includes:

**Server**
* IPv4 **and** IPv6 support
* Create/Delete/Modify
* Start/Stop/Restart server
* Import existing configurations
* Export server config, along with client config as zip.

**Peer**
* Create/Delete/Modify
* Bandwidth usage statistics
* Export by QRCode, Text

**General**
* Modify Admin User

# Dependencies
* Linux >= 5.6 *(Alternatively: wireguard-dkms)*

# Common Installation Steps
1. Enable ip forwarding:
     ```
    sysctl -w net.ipv4.ip_forward=1 # IPV4 Support
    sysctl -w net.ipv6.conf.all.forwarding=1  # IPV6 Support
     ```
2. For persistent configuration: 
    ```
    cat > /etc/sysctl.d/99-sysctl.conf << EOF
    net.ipv4.ip_forward = 1
    net.ipv6.conf.all.forwarding=1
    EOF
    ```
3. It is recommended to have a firewall protecting your servers

## Notes
* A few people has experienced issues with running the dockerized method using bridged networking. To fix this, you can use `network_mode: host`. Note that you can no longer reverse-proxy the web interface from reverse proxies such as [jwilder/nginx-proxy](https://hub.docker.com/r/jwilder/nginx-proxy/).

## Method #1: Docker-compose
```yaml
version: "2.1"
services:
  wireguard:
    container_name: wg-manager
    image: perara/wg-manager
    restart: always
    sysctls:
      net.ipv6.conf.all.disable_ipv6: 0  # Required for IPV6
    cap_add:
      - NET_ADMIN
    #network_mode: host # Alternatively
    ports:
       - 51800-51900:51800-51900/udp
       - 8888:8888
    volumes:
      - ./wg-manager:/config
    environment:
      HOST: 0.0.0.0
      PORT: 8888
      ADMIN_PASSWORD: admin
      ADMIN_USERNAME: admin
      WEB_CONCURRENCY: 1
```
or [plain docker here](./docs/guides/docker_configuration.md)

# Method #2: Bare Metal
- [Installation on Debian/Ubuntu/RPI4](./docs/install.md)

# Using the development branch
As there is no builds for the development branch, you have to do the following:
Change `image: perara/wg-manager` to
```
build:
      context: https://github.com/perara/wg-manager.git#dev
```

# Guides
- [Importing Existing configuration](./docs/guides/import_existing_server.md)
- [Reverse Proxy](./docs/guides/reverse_proxy.md)

# Usage
When docker container/server has started, go to http://localhost:8888

# API Docs
The API docs is found [here](./docs/api.md).

# Environment variables
| Environment      | Description                                                               | Recommended |
|------------------|---------------------------------------------------------------------------|-------------|
| GUNICORN_CONF    | Location of custom gunicorn configuration                                 | default     |
| WORKERS_PER_CORE | How many concurrent workers should there be per available core (Gunicorn) | default     |
| WEB_CONCURRENCY  | The number of worker processes for handling requests. (Gunicorn)          | 1           |
| HOST             | 0.0.0.0 or unix:/tmp/gunicorn.sock if reverse proxy. Remember to mount    | 0.0.0.0     |
| PORT             | The port to use if running with IP host bind                              | 80          |
| LOG_LEVEL        | Logging level of gunicorn/python                                          | info        |
| ADMIN_USERNAME   | Default admin username on database creation                               | admin       |
| ADMIN_PASSWORD   | Default admin password on database creation                               | admin       |
| POST_UP          | The POST_UP Command (version 4)                                           | default     |
| POST_DOWN        | The POST_DOWN Command (version 4)                                         | default     |
| POST_UP_V6       | The POST_UP Command (version 6)                                           | default     |
| POST_DOWN_V6     | The POST_DOWN Command (version 6)                                         | default     |

# Showcase
![Illustration](docs/images/0.png)

![Illustration](docs/images/1.png)

![Illustration](docs/images/2.png)

![Illustration](docs/images/3.png)

![Illustration](docs/images/4.png)

![Illustration](docs/images/5.png)

![Illustration](docs/images/6.png)

![Illustration](docs/images/7.png)

![Illustration](docs/images/8.png)

# Roadmap
### Primaries
- Implement multi-server support (setting up site-2-site servers from the GUI)
- Extending multi-server support to enable custom access lists (A peer can be assigned to multiple servers, as part of the ACL)

### Other
* Eventual bugfixes
* Improve Auth
* Improve everything...
