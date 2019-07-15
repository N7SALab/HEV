# HEV
Hunting EnVironment - Gather everything. Analyze everything. 

#### build

- `cp hev-example.env hev.env`

hev-example.env:

Environment Variable | Use
-|-
ELASTICSEARCH_HOSTS| Elasticsearch servers (separated by spaces)
NEO4J_USER| Neo4j user
NEO4J_PASSWORD| Neo4j password
NEO4J_SERVERS_LIST| Neo4j servers (separated by spaces)
MINIO_HOST| Minio server
MINIO_ACCESS_KEY| Minio access key
MINIO_SECRET_KEY| Minio secret key
MINIO_HEV_HOST| Minio server for HEV functionality
MINIO_HEV_ACCESS_KEY| Minio hev access key
MINIO_HEV_SECRET_KEY| Minio hev secret key
MINIO_PUB_HOST| Minio public server
MINIO_PUB_ACCESS_KEY| Minio public access key 
MINIO_PUB_SECRET_KEY| Minio public secret key
OPENVPN| OpenVPN server name
OPENVPN_BUCKET| OpenVPN minio bucket name
OPENVPN_CONFIGS| OpenVPN config directory name (need example)
INSTAGRAM_USER| Instagram user
INSTAGRAM_PASSWORD| Instagram password
INSTAGRAM_FOLLOWING_LIST| List of accounts to follow (seprated by space)

then

```
./build.sh
```

#### test
```
source hev.env
./tests.sh
```

#### run
```
source hev.env
python3 run_hev.py
```
