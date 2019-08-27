import json


def test_conf():
    try:
        json.load(open('/hev/hev-conf.json'))
    except:
        json.load(open('../hev-conf.json'))
