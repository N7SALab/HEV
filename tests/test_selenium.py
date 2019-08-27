import json
import warnings

from core.helpers import minio

from core.helpers.selenium import (Browser, chrome_sandboxed, chrome_remote,
                                   chrome_headless_sandboxed, chrome_for_docker, chrome,
                                   chrome_headless_nosandbox,
                                   chrome_nosandbox)

try:
    CONF = json.load(open('hev.conf'))
except:
    CONF = json.load(open('../hev.conf'))


def test_chrome_for_docker():
    browser = chrome_for_docker()
    browser.quit()


def disabled_test_chrome():
    browser = chrome()
    browser.quit()


def disabled_test_chrome_sandboxed():
    browser = chrome_sandboxed()
    browser.quit()


def disabled_test_chrome_nosandbox():
    browser = chrome_nosandbox()
    browser.quit()


def test_chrome_headless_nosandbox():
    browser = chrome_headless_nosandbox()
    browser.quit()


def disabled_test_chrome_headless_sandboxed():
    browser = chrome_headless_sandboxed()
    browser.quit()


def disabled_test_chrome_remote():
    browser = chrome_remote()
    browser.quit()


def test_save_screenshot_to_public_minio():
    browser = Browser(chrome_headless_nosandbox())
    browser.new_resolution(device_type='1024x768')
    browser.browser.get('http://reddit.com/')
    assert browser.save_screenshot_to_public_minio(prefix='hello')
    browser.quit()


def test_save_screenshot_to_minio():
    client = minio.client(CONF['minio-hev'], secure=False)
    assert client is not None

    browser = Browser(chrome_headless_nosandbox())
    browser.new_resolution(device_type='1024x768')
    browser.browser.get('http://reddit.com/')
    browser.set_minio_client(client)
    assert browser.save_screenshot_to_minio()
    browser.quit()


def test_save_screenshot_to_file():
    browser = Browser(chrome_headless_nosandbox())
    browser.new_resolution(device_type='1024x768')
    assert browser.save_screenshot_to_file('http://1.1.1.1')
    browser.quit()


def test_click():
    browser = Browser(chrome_for_docker())
    browser.browser.get('https://reddit.com')
    browser.save_screenshot_to_file()
    browser.click('//*[@id="USER_DROPDOWN_ID"]')
    browser.save_screenshot_to_file()
    browser.click('/html/body/div[4]/div/button')
    browser.save_screenshot_to_file()
    browser.quit()


def test_type():
    warnings.warn('Test not implemented', Warning)
    browser = Browser(chrome_for_docker())
    browser.quit()


if __name__ == "__main__":
    test_save_screenshot_to_file()
