import socket

from minio import Minio
from urllib.parse import urlparse

from core.helpers.log import hevlog

hevlog = hevlog('minio', level='error')


class Wrapper:

    def __init__(self, endpoint, access_key=None,
                 secret_key=None,
                 session_token=None,
                 secure=True,
                 region=None,
                 http_client=None):
        self.Minio = Minio(endpoint, access_key=access_key,
                           secret_key=secret_key,
                           session_token=session_token,
                           secure=secure,
                           region=region,
                           http_client=http_client)

    def download_object(self, bucket, file):
        """ Minio object downloader
        """
        hevlog.logging.debug('[downloader] Downloading: {}/{}'.format(bucket, file.object_name))
        return self.Minio.get_object(bucket, file.object_name)

    def list_all_objects(self, bucket, folder, recursive=True):
        """ List Minio objects
        """
        hevlog.logging.debug('[list_all_objects] bucket: {}, folder: {}'.format(bucket, folder))
        return self.Minio.list_objects_v2(bucket, folder, recursive=recursive)

    def put_object(self, bucket_name, object_name, data, length,
                   content_type='application/octet-stream',
                   metadata=None, sse=None, progress=None,
                   part_size=None):
        """ Minio object uploader
        """

        hevlog.logging.debug('[put_object] Uploading: {}'.format(object_name))
        try:
            self.Minio.put_object(bucket_name, object_name, data, length,
                                  content_type=content_type,
                                  metadata=metadata, sse=sse, progress=progress)
            hevlog.logging.info(
                '[put_object] Saved to {}/{}/{}'.format(self.Minio._endpoint_url, bucket_name, object_name))

        except:
            hevlog.logging.error(
                '[put_object] Unable to save {}/{}/{}'.format(self.Minio._endpoint_url, bucket_name, object_name))

    def make_bucket(self, bucket_name):
        try:
            self.Minio.make_bucket(bucket_name)
            hevlog.logging.debug('[make_bucket] Created bucket: {}'.format(bucket_name))
        except:
            hevlog.logging.debug('[make_bucket] Bucket exists: {}'.format(bucket_name))


def client(MINIO_CONF, secure=True, session_token=None, region=None, http_client=None):
    for host in MINIO_CONF['host']:
        endpoint = urlparse(host)
        if check_connection(endpoint.hostname, endpoint.port):
            return Wrapper(endpoint=endpoint.netloc,
                           access_key=MINIO_CONF['access_key'],
                           secret_key=MINIO_CONF['secret_key'],
                           secure=secure,
                           session_token=session_token,
                           region=region,
                           http_client=http_client)


def check_connection(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        return True
    except:
        return False


def use_public_server():
    return Wrapper('play.minio.io:9000', 'Q3AM3UQ867SPQQA43P2F',
                   'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')
