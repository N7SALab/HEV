import json

from modules import instagram

try:
    CONF = json.load(open('hev.conf'))
except:
    CONF = json.load(open('../hev.conf'))


def test_run():
    # instagram.run(CONF['instagram'])
    instagram.test_run(CONF['instagram'])


if __name__ == "__main__":
    test_run()
