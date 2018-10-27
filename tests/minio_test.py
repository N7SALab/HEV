import os
import io
import json

from minio import Minio

from core.helpers.log import log


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


minioClient = Minio(CONF['config']['minio']['host'],
                    access_key=CONF['config']['minio']['access_key'],
                    secret_key=CONF['config']['minio']['secret_key'],
                    secure=False)

bucket = CONF['config']['minio']['bucket']
folder = CONF['config']['minio']['folder']
client_configs = CONF['config']['minio']['client_configs']


class ClientConfig:
    """ Create an OpenVPN client config

    """

    def __init__(self, name, conf):
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

        log('Creating new OpenVPN client config')

        server = conf['config']['minio']['host']

        self.name = name

        self.config = 'client\n'
        self.config += 'dev tun\n'
        self.config += 'remote {}\n'.format(server)
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
        self.config += 'port 1194\n'
        self.config += 'proto udp\n'
        self.config += 'cipher BF-CBC\n'
        self.config += 'comp-lzo\n'
        self.config += 'remote-cert-tls server\n'

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
        self.ta = '{}\n{}\n{}\n'.format('<ta>', ta.decode(), '</ta>')

    def build_config(self):

        config = self.config
        config += self.ca
        config += self.cert
        config += self.key
        config += self.ta

        filename = self.name + '.ovpn'

        return filename, io.BytesIO(config.encode()), len(config)


ca = None
cert = []
key = []
ta = None

log('Collecting all Minio bucket files')

for file in minioClient.list_objects_v2(bucket, folder, recursive=True):

    file_path, file_name = os.path.split(file.object_name)
    folder = file_path.split('/')[-1]

    if file_name == 'ca.crt':
        download = minioClient.get_object(bucket, file.object_name)
        data = download.data
        ca = data

    if file_name == 'ta.key':
        download = minioClient.get_object(bucket, file.object_name)
        data = download.data
        ta = data

    if folder == 'issued':
        download = minioClient.get_object(bucket, file.object_name)
        data = download.data
        cert.append((file_name, data))

    if folder == 'private':
        download = minioClient.get_object(bucket, file.object_name)
        data = download.data
        key.append((file_name, data))


for user, data in cert:
    name, _ = os.path.splitext(user)
    config = ClientConfig(name, CONF)
    config.add_ca(ca)
    config.add_ta(ta)
    config.add_cert(data)

    for k in key:
        k_name, k_data = k
        k_name, _ = os.path.splitext(k_name)

        if name == k_name:
          config.add_key(k_data)

    config_name, config_data, config_len = config.build_config()

    minioClient.put_object(bucket, client_configs + config_name, config_data, config_len)

    log('OpenVPN client config created: {}'.format(config_name))
