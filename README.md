# wireguard-manager
The wireguard-manager provides a easy-to-use graphical interface to setup and manage wireguard server(s).
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
* docker

# Installation
```bash
docker run -d \
--cap-add NET_ADMIN \
--name wireguard-manager \
--net host \
-v wireguard-manager:/config \
-e PORT="8888" \
perara/wireguard-manager
```

# Usage
When docker container is started, go to http://localhost:80


# Showcase
![Illustration](docs/images/1.png)

![Illustration](docs/images/2.png)

![Illustration](docs/images/3.png)

![Illustration](docs/images/4.png)

# Roadmap
* Add some insecure authentication
* Eventual bugfixes
