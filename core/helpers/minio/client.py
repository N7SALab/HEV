from minio import Minio


def Client(CONF):
    return Minio(CONF['host'],
                 access_key=CONF['access_key'],
                 secret_key=CONF['secret_key'],
                 secure=False)
