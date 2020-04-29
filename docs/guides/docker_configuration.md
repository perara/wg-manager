# Docker Configuration
```bash
docker run -d \
--cap-add NET_ADMIN \
--name wg-manager \
#--net host \
-p "51800-51900:51800-51900/udp" \
-p "8888:8888" \
-v wg-manager:/config \
-e PORT="8888" \
-e ADMIN_USERNAME="admin" \
-e ADMIN_PASSWORD="admin" \
perara/wg-manager
```
