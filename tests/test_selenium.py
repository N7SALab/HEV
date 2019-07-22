import json

from core.helpers.sleep import sleeper

from core.helpers import minio

from core.helpers.selenium.browser import (
    Browser,
    chrome_headless_nosandbox,
    chrome_headless_sandboxed,
    chrome_sandboxed,
    chrome_remote,
    chrome
)

try:
    CONF = json.load(open('hev.conf'))
except:
    CONF = json.load(open('../hev.conf'))


def disabled_test_chrome():
    browser = chrome()
    browser.close()
    browser.quit()
    browser.stop_client()


def disabled_test_chrome_sandboxed():
    browser = chrome_sandboxed()
    browser.close()
    browser.quit()
    browser.stop_client()


def test_chrome_headless_nosandbox():
    browser = chrome_headless_nosandbox()
    browser.close()
    browser.quit()
    browser.stop_client()


def disabled_test_chrome_headless_sandboxed():
    browser = chrome_headless_sandboxed()
    browser.close()
    browser.quit()
    browser.stop_client()


def disabled_test_chrome_remote():
    browser = chrome_remote()
    browser.close()
    browser.quit()
    browser.stop_client()


def test_save_screenshot_to_public_minio():
    browser = Browser(chrome_headless_nosandbox())
    browser.new_resolution(device_type='pixel3')
    browser.selenium.get('http://reddit.com/')
    assert browser.save_screenshot_to_public_minio()
    browser.selenium.close()
    browser.selenium.quit()
    browser.selenium.stop_client()


def test_save_screenshot_to_minio():
    client = minio.client(CONF['minio-hev'], secure=False)
    assert client is not None

    browser = Browser(chrome_headless_nosandbox())
    browser.new_resolution(device_type='pixel3')
    browser.selenium.get('http://reddit.com/')
    assert browser.save_screenshot_to_minio(client)
    browser.selenium.close()
    browser.selenium.quit()
    browser.selenium.stop_client()


if __name__ == "__main__":
    browser = chrome()
    browser.close()
    browser.quit()
    browser.stop_client()
