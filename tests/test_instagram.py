import json

from modules import instagram

try:
    CONF = json.load(open('hev-conf.json'))
except:
    try:
        CONF = json.load(open('../hev-conf.json'))
    except:
        CONF = json.load(open('/hev/hev-conf.json'))


def test_run():
    # instagram.run(CONF)
    instagram.test_run(CONF)


if __name__ == "__main__":
    test_run()
