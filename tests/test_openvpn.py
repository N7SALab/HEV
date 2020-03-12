import json

from modules.openvpn import Openvpn
from core.helpers.config import Config

CONF = Config()


def test_openpvn():
    assert Openvpn.build_client_configs_test(
        CONF.MINIO_HOST,
        CONF.MINIO_ACCESS_KEY,
        CONF.MINIO_SECRET_KEY,
        CONF.OPENVPN) is True
