import json

from modules import instagram


def test_run():
    CONF = json.load(open('hev.conf'))
    instagram.test_run(CONF['instagram'])


if __name__ == "__main__":
    test_run()
