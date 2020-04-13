# Docker Configuration
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
