import json

from modules import openvpn

try:
    CONF = json.load(open('hev.conf'))
except:
    CONF = json.load(open('../hev.conf'))


def test_openpvn():
    assert openvpn.test_run(CONF['minio'], CONF['openvpn']) is True
