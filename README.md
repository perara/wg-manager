# wg-manager
The wg-manager provides a easy-to-use graphical interface to setup and manage WireGuard server(s).
The following features is implemented:
* Create/Delete/Modify Server
* Create/Delete/Modify Users
* QRCode export
* Text export
* Start/Stop server
* User bandwidth usage statistics

The interface runs in docker and requires the host to have installed wireguard, either as a dkms module, or by using newer kernels (5.6+)

# Dependencies
* wireguard-dkms or Linux kernel >= 5.6
* python 3.6+

# Installation (Docker)
1. Enable ip forwarding with `sysctl -w net.ipv4.ip_forward=1`
1.1. To make the forwarding persistent add `net.ipv4.ip_forward = 1` to `/etc/sysctl.d/99-sysctl.conf`
2. It is recommended to have a firewall protecting your services
## Docker
```bash
docker run -d \
--cap-add NET_ADMIN \
--name wireguard-manager \
--net host \
-p "51800-51900:51800-51900/udp" \
-v wireguard-manager:/config \
-e PORT="8888" \
-e ADMIN_USERNAME="admin" \
-e ADMIN_PASSWORD="admin" \
perara/wireguard-manager
```

## Docker-compose
```yaml
version: "2"
services:
 wireguard:
    container_name: wireguard-manager
    image: perara/wireguard-manager
    cap_add:
      - NET_ADMIN
    ports:
       - 51800:51900/udp
       - 8888:8888
    volumes:
      - ./ops/wireguard/_data:/config
    environment:
      HOST: 0.0.0.0
      PORT: 8888
      ADMIN_PASSWORD: admin
      ADMIN_USERNAME: admin
      WEB_CONCURRENCY: 1
    network_mode: host
```

# Install (OS)
- [Installation on Debian/Ubuntu](./docs/install_debian.md) (TODO)
- [Installation on Raspberry PI 4](./docs/install_rpi.md)

# Environment variables
| Environment      | Description                                                              | Recommended |
|------------------|--------------------------------------------------------------------------|-------------|
| GUNICORN_CONF    | Location of custom gunicorn configuration                                | default     |
| WORKERS_PER_CORE | How many concurrent workers should there be per available core (Gunicorn | default     |
| WEB_CONCURRENCY  | The number of worker processes for handling requests. (Gunicorn)         | 1           |
| HOST             | 0.0.0.0 or unix:/tmp/gunicorn.sock if reverse proxy. Remember to mount   | 0.0.0.0     |
| PORT             | The port to use if running with IP host bind                             | 80          |
| LOG_LEVEL        | Logging level of gunicorn/python                                         | info        |
| ADMIN_USERNAME   | Default admin username on database creation                              | admin       |
| ADMIN_PASSWORD   | Default admin password on database creation                              | admin       |


# Usage
When docker container is started, go to http://localhost:80

### Importing existing configuration
1. Click the Import configuration button in the right pane
2. Select all relevant server and client files. There is a few cases here:
    1. If you only provide a server configuration. Everything will load fine, but you cannot export peer.configurations
    2. If you provide both client and server configurations. Everything should work ok
    3. Client should have [Interface] and [Peer] defined. Currently only supporting clients with 1 peer section.

# Reverse Proxy
Use jwilder/nginx-proxy or similar.


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
