import socket

from minio import Minio
from urllib.parse import urlparse

from core.helpers.hevlog import Hevlog
from core.helpers.networking import Networking

hevlog = Hevlog('minio', level='info')


class MinioWrapper:

    def __init__(self, MINIO_CONF, secure=True, session_token=None, region=None, http_client=None):
        for host in MINIO_CONF['host']:
            endpoint = urlparse(host)
            if Networking.check_connection(endpoint.hostname, endpoint.port):
                self.Minio = Minio(endpoint=endpoint.netloc,
                                   access_key=MINIO_CONF['access_key'],
                                   secret_key=MINIO_CONF['secret_key'],
                                   secure=secure,
                                   session_token=session_token,
                                   region=region,
                                   http_client=http_client)

                self.connected = True
                break
        else:
            self.connected = False

    def download_object(self, bucket_name, file):
        """ Minio object downloader
        """
        hevlog.logging.debug('[downloader] Downloading: {}/{}'.format(bucket_name, file.object_name))
        return self.Minio.get_object(bucket_name, file.object_name)

    def list_all_objects(self, bucket_name, folder=None, recursive=True):
        """ List Minio objects
        """
        hevlog.logging.debug('[list_all_objects] bucket: {}, folder: {}'.format(bucket_name, folder))
        return self.Minio.list_objects_v2(bucket_name, folder, recursive=recursive)

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

            return True

        except:
            hevlog.logging.error(
                '[put_object] Unable to save {}/{}/{}'.format(self.Minio._endpoint_url, bucket_name, object_name))

            return False

    def clear_bucket(self, bucket_name, folder=None):
        objects = self.list_all_objects(bucket_name, folder)

        for Object in objects:
            name = Object.object_name
            self.Minio.remove_object(bucket_name, name)
            hevlog.logging.info('deleted {}'.format(name))

    def remove_object(self, bucket_name, Object):
        self.Minio.remove_object(bucket_name, Object.object_name)
        hevlog.logging.debug('deleted {}'.format(Object.name))

    def make_bucket(self, bucket_name):
        try:
            self.Minio.make_bucket(bucket_name)
            hevlog.logging.debug('[make_bucket] Created bucket: {}'.format(bucket_name))

            return True

        except:
            hevlog.logging.debug('[make_bucket] Bucket exists: {}'.format(bucket_name))

            return False


def use_public_server():
    return MinioWrapper({
        "host": ["https://play.min.io:9000"],
        "access_key": "Q3AM3UQ867SPQQA43P2F",
        "secret_key": "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
    })
