import json

from modules.instagram import Instagram
from core.helpers.selenium import Browser, chrome, chrome_for_docker

configs = [
    'hev-conf.json',
    '../hev-conf.json',
    '/hev/hev-conf.json'
]

for c in configs:
    try:
        CONF = json.load(open(c))
    except:
        pass


def test_run():
    Instagram(CONF, browser=Browser(chrome_for_docker())).run_stories(limit=1)


def disabled_test_run_with_browser():
    Instagram(CONF, browser=Browser(chrome())).run_stories(limit=1)


if __name__ == "__main__":
    test_run()
