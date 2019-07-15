from minio import Minio


def Client(MINIO_CONF):
    return Minio(MINIO_CONF['host'],
                 access_key=MINIO_CONF['access_key'],
                 secret_key=MINIO_CONF['secret_key'],
                 secure=False)
