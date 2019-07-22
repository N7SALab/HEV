import json

from modules import instagram

try:
    CONF = json.load(open('hev.conf'))
except:
    CONF = json.load(open('../hev.conf'))


def test_run():
    # instagram.run(CONF)
    instagram.test_run(CONF)


if __name__ == "__main__":
    test_run()
