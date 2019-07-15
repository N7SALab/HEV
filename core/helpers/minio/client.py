import socket

from urllib.parse import urlparse
from minio import Minio

from core.helpers.log import hevlog

hevlog = hevlog('minio', level='error')


def Client(MINIO_CONF):
    for host in MINIO_CONF['host']:
        p = urlparse(host)
        if check_socket(p.hostname, p.port):
            return Minio(p.netloc,
                         access_key=MINIO_CONF['access_key'],
                         secret_key=MINIO_CONF['secret_key'],
                         secure=False)


def check_socket(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        return True
    except:
        return False
