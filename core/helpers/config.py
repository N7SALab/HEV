import os


class Config:

    def __init__(self):
        self.NEO4J_USER = os.getenv('NEO4J_USER')
        self.NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
        self.NEO4J_SERVERS_LIST = os.getenv('NEO4J_SERVERS_LIST')

        self.MINIO_HOST = os.getenv('MINIO_HOST')
        self.MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
        self.MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')

        self.MINIO_HEV_HOST = os.getenv('MINIO_HOST_HEV')
        self.MINIO_HEV_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY_HEV')
        self.MINIO_HEV_SECRET_KEY = os.getenv('MINIO_SECRET_KEY_HEV')

        self.MINIO_PUB_HOST = os.getenv('MINIO_HOST_PUB')
        self.MINIO_PUB_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY_PUB')
        self.MINIO_PUB_SECRET_KEY = os.getenv('MINIO_SECRET_KEY_PUB')

        self.OPENVPN = os.getenv('OPENVPN')
        self.OPENVPN_BUCKET = os.getenv('OPENVPN_BUCKET')
        self.OPENVPN_CONFIGS = os.getenv('OPENVPN_CONFIGS')

        self.ELASTICSEARCH_HOSTS = os.getenv('ELASTICSEARCH_HOSTS')

        self.INSTAGRAM = os.getenv('INSTAGRAM')
        self.INSTAGRAM_USER = os.getenv('INSTAGRAM_USER')
        self.INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
        self.INSTAGRAM_FOLLOWING_LIST = os.getenv('INSTAGRAM_FOLLOWING_LIST')
