# Build Docker Image from Github Repo
The steps below will walk you through installing the application in a docker container from the latest github version.

---

First thing we need to do is clone the github repository
```bash
git clone https://github.com/perara/wg-manager.git
```

Next we need to build the image. This will take some time.
```bash
docker build -t wg-manager .
```

Now that our image is built, we can either launch the container via _docker-compose_ or through the _docker CLI_.

## Docker Compose
```yaml
version: "2.1"
services:
  wireguard:
    container_name: wg-manager
    image: wg-manager
    restart: always
    sysctls:
      net.ipv6.conf.all.disable_ipv6: 0  # Required for IPV6
    cap_add:
      - NET_ADMIN
    network_mode: host
    ports:
       - 51802:51802/udp
       - 8888:8888
    volumes:
      - ./wg-manager:/config
    environment:
      HOST: 0.0.0.0
      PORT: 8888
      ADMIN_USERNAME: admin
      ADMIN_PASSWORD: admin
      WEB_CONCURRENCY: 1
```

## Docker CLI
```bash
docker run -d \
--sysctl net.ipv6.conf.all.disable_ipv6=0 \
--cap-add NET_ADMIN \
--name wg-manager \
--net host \
-p "51802:51802/udp" \
-p "8888:8888" \
-v wg-manager:/config \
-e HOST="0.0.0.0" \
-e PORT="8888" \
-e ADMIN_USERNAME="admin" \
-e ADMIN_PASSWORD="admin" \
wg-manager
```
