import json
from core.helpers import minio


def test_client():
    CONF = json.load(open('hev.conf'))
    assert minio.Client(CONF['minio'])
