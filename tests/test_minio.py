import io
import json
import datetime

from core.helpers import minio
from core.helpers.networking import Networking

try:
    CONF = json.load(open('hev-conf.json'))
except:
    try:
        CONF = json.load(open('../hev-conf.json'))
    except:
        CONF = json.load(open('/hev/hev-conf.json'))


def test_MinioWrapper():
    assert minio.MinioWrapper(CONF['minio'], secure=False).Minio.list_buckets() is not None
    assert minio.MinioWrapper(CONF['minio'], secure=False).connected is True
    assert minio.MinioWrapper(CONF['minio-pub'], secure=False).connected is True
    assert minio.MinioWrapper(CONF['minio-hev'], secure=False).connected is True
    assert minio.MinioWrapper(
        {
            "host": ["http://minio.0000000"],
            "access_key": "none",
            "secret_key": "none"
        }, secure=False).connected is False


def test_check_connection():
    assert Networking.check_connection('google.com', 80) is True
    assert Networking.check_connection('minio.0000000', 9000) is False


def test_client():
    assert minio.MinioWrapper(CONF['minio'], secure=False) is not None


def test_public_upload():
    bucket_name = 'mymymymymytesting'
    object_name = 'test.txt'
    data = io.BytesIO(bytes(str(datetime.datetime.now()).encode()))
    length = data.getvalue().__len__()

    public_minio = minio.use_public_server()
    try:
        public_minio.Minio.make_bucket(bucket_name)
    except:
        pass
    public_minio.Minio.put_object(bucket_name, object_name, data, length)


def test_clear_bucket():
    client = minio.MinioWrapper(CONF['minio-hev'], secure=False)
    bucket_name = 'testing'
    client.clear_bucket(bucket_name)
    bucket_name = 'screenshots'
    client.clear_bucket(bucket_name)


if __name__ == "__main__":
    test_clear_bucket()

    assert minio.MinioWrapper(
        {
            "host": ["http://minio.0000000"],
            "access_key": "none",
            "secret_key": "none"
        }, secure=False).connected is False
    pass
