import os
import io

from core.helpers import minio
from core.helpers.log import hevlog
from core.helpers.sleep import sleeper

hevlog = hevlog('openvpn', level='info')


class ClientConfig:
    """ Create an OpenVPN client config
    """

    def __init__(self, name, hosts, options=None):
        """
        client
        dev tun
        remote example.com
        resolv-retry infinite
        nobind
        persist-key
        persist-tun
        ca [inline]
        cert [inline]
        key [inline]
        tls-auth [inline] 1
        verb 1
        keepalive 10 120
        port 1194
        proto udp
        cipher BF-CBC
        comp-lzo
        remote-cert-tls server

        <ca>
        </ca>

        <cert>
        </cert>

        <key>
        </key>

        <tls-auth>
        </tls-auth>
        """

        hevlog.logging.debug('[ClientConfig] Creating new OpenVPN client config')

        self.name = name

        self.config = 'client\n'
        self.config += 'dev tun\n'

        for host in hosts:
            host, port, conn = host.split(':')
            self.config += 'remote {} {} {}\n'.format(host, port, conn)

        self.config += 'resolv-retry infinite\n'
        self.config += 'nobind\n'
        self.config += 'persist-key\n'
        self.config += 'persist-tun\n'
        self.config += 'ca [inline]\n'
        self.config += 'cert [inline]\n'
        self.config += 'key [inline]\n'
        self.config += 'tls-auth [inline] 1\n'
        self.config += 'verb 1\n'
        self.config += 'keepalive 10 120\n'
        self.config += 'cipher BF-CBC\n'
        self.config += 'comp-lzo\n'
        self.config += 'remote-cert-tls server\n'
        self.config += 'key-direction 1\n'

        if options:
            for option in options:
                self.config += option

        self.CONFIG = self.config.split('\n')

        self.ca = None
        self.cert = None
        self.key = None
        self.ta = None

    def add_ca(self, ca):
        self.ca = '{}\n{}\n{}\n'.format('<ca>', ca.decode(), '</ca>')

    def add_cert(self, cert):
        self.cert = '{}\n{}\n{}\n'.format('<cert>', cert.decode(), '</cert>')

    def add_key(self, key):
        self.key = '{}\n{}\n{}\n'.format('<key>', key.decode(), '</key>')

    def add_ta(self, ta):
        self.ta = '{}\n{}\n{}\n'.format('<tls-auth>', ta.decode(), '</tls-auth>')

    def build_config(self, prefix):

        config = self.config
        config += self.ca
        config += self.cert
        config += self.key
        config += self.ta

        if prefix:
            filename = prefix + '-' + self.name + '.ovpn'
        else:
            filename = self.name + '.ovpn'

        return filename, io.BytesIO(config.encode()), len(config)


def list_objects(minioClient, bucket, folder, recursive=True):
    """ List Minio objects
    """
    return minioClient.list_objects_v2(bucket, folder, recursive=recursive)


def collector(minioClient, bucket, folder):
    """ Collect required files to build an OpenVPN client
    """
    hevlog.logging.debug('[collector] Collecting all Minio bucket files')

    ca = None
    cert = []
    key = []
    ta = None

    for file in list_objects(minioClient, bucket, folder):

        file_path, file_name = os.path.split(file.object_name)
        folder = file_path.split('/')[-1]

        if file_name == 'ca.crt':
            download = downloader(minioClient, bucket, file)
            data = download.data
            ca = data

        if file_name == 'ta.key':
            download = downloader(minioClient, bucket, file)
            data = download.data
            ta = data

        if folder == 'issued':
            download = downloader(minioClient, bucket, file)
            data = download.data
            cert.append((file_name, data))

        if folder == 'private':
            download = downloader(minioClient, bucket, file)
            data = download.data
            key.append((file_name, data))

    return ca, cert, key, ta


def put_object(minioClient, bucket, client_configs, config_name, config_data, config_len):
    """ Minio object uploader
    """
    hevlog.logging.debug('[put_object] Uploading: {}'.format(config_name))
    return minioClient.put_object(bucket, '{}/{}'.format(client_configs, config_name), config_data, config_len)


def downloader(minioClient, bucket, file):
    """ Minio object downloader
    """
    hevlog.logging.debug('[downloader] Downloading: {}/{}'.format(bucket, file.object_name))
    return minioClient.get_object(bucket, file.object_name)


def creator(minioClient, bucket, client_configs, ca, cert, key, ta, hosts, prefix, options=None):
    """ Create and upload OpenVPN Client config
    """
    for user, data in cert:
        name, _ = os.path.splitext(user)
        config = ClientConfig(name, hosts, options)
        config.add_ca(ca)
        config.add_ta(ta)
        config.add_cert(data)

        for k in key:
            k_name, k_data = k
            k_name, _ = os.path.splitext(k_name)

            if name == k_name:
              config.add_key(k_data)

        config_name, config_data, config_len = config.build_config(prefix)

        put_object(minioClient, bucket, client_configs, config_name, config_data, config_len)

        hevlog.logging.debug('[creator] OpenVPN client config uploaded: {}'.format(config_name))


def run(minio_config):

    while True:
        minioClient = minio.Client(minio_config)

        minio_bucket = minio_config['bucket']
        openvpn_configs = minio_config['openvpn']

        for config in openvpn_configs:
            hosts = config['hosts']
            folder = config['folder']
            keys = folder + '/pki'
            client_configs = folder + '/configs'
            try:
                prefix = config['prefix']
            except:
                prefix = None
            try:
                options = config['options']
            except:
                options = None

            ca, cert, key, ta = collector(minioClient, minio_bucket, keys)
            creator(minioClient, minio_bucket, client_configs, ca, cert, key, ta, hosts, prefix, options)

        hevlog.logging.info('[build client configs] Finshed building all OpenVPN clients')
        hevlog.logging.debug('[ClientConfig] sleeping')
        sleeper.day('openvpn')
