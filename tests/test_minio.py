import json
from core.helpers import minio


def test_Client():
    CONF = json.load(open('hev.conf'))
    minio.Client(CONF['minio'])


def test_check_socket():
    # CONF = json.load(open('hev.conf'))
    minio.check_socket('minio', 9000)
    minio.check_socket('rancher.n7sa.com', 9001)
