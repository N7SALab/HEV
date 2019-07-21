import json


def test_conf():
    try:
        json.load(open('../hev.conf'))
    except:
        json.load(open('hev.conf'))
