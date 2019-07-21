import io
import json
import datetime

from core.helpers import minio

try:
    CONF = json.load(open('hev.conf'))
except:
    CONF = json.load(open('../hev.conf'))

public_minio = minio.Wrapper('play.minio.io:9000', 'Q3AM3UQ867SPQQA43P2F',
                             'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')


def test_Client():
    assert minio.client(CONF['minio'], secure=False).Minio.list_buckets() is not None
    assert minio.client(CONF['minio'], secure=False) is not None
    assert minio.client(CONF['minio-pub'], secure=False) is not None
    assert minio.client(CONF['minio-hev'], secure=False) is not None
    assert minio.client(
        {
            "host": ["minio.0000000"],
            "access_key": "none",
            "secret_key": "none"
        }, secure=False) is None


def test_check_connection():
    assert minio.check_connection('google.com', 80) is True
    assert minio.check_connection('minio.0000000', 9000) is False


def test_client():
    assert minio.client(CONF['minio'], secure=False) is not None


def test_Wrapper():
    assert minio.Wrapper('minio.000000', access_key=None,
                         secret_key=None,
                         session_token=None,
                         secure=True,
                         region=None,
                         http_client=None).Minio is not None


def test_public_upload():
    bucket_name = 'mymymymymy'
    object_name = 'file.txt'
    data = io.BytesIO(bytes(str(datetime.datetime.now()).encode()))
    length = data.getvalue().__len__()

    try:
        public_minio.Minio.make_bucket(bucket_name)
    except:
        pass
    public_minio.put_object(bucket_name, object_name, data, length)
