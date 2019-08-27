import json

from modules import openvpn

try:
    CONF = json.load(open('hev-conf.json'))
except:
    try:
        CONF = json.load(open('../hev-conf.json'))
    except:
        CONF = json.load(open('/hev/hev-conf.json'))


def test_openpvn():
    assert openvpn.build_client_configs_test(CONF['minio'], CONF['openvpn']) is True
