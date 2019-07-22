import os
import io
import warnings
import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from core.helpers.log import hevlog
from core.helpers.sleep import sleeper

from core.helpers.minio import use_public_server

hevlog = hevlog('selenium', level='info')


class Browser:

    def __init__(self, browser=None, webdriver=webdriver):
        self.webdriver = webdriver
        self.browser = browser if browser else self.webdriver.Chrome()
        self.minio_client = None

    def set_minio_client(self, minio_client):
        self.minio_client = minio_client

    def save_screenshot_to_minio(self, url=None, bucket_name='testing', object_name=None):

        if not self.minio_client:
            return False

        if not object_name:
            timestamp = str(datetime.datetime.now().isoformat()).replace(':', '_')
            object_name = 'screenshot-{}.png'.format(timestamp)
        else:
            object_name = 'screenshot.png'

        if url:
            self.browser.get(url)

        sleeper.seconds('Loading page', 4)

        bucket_name = bucket_name
        object_name = object_name
        data = io.BytesIO(self.browser.get_screenshot_as_png())
        length = data.getvalue().__len__()

        private_minio = self.minio_client
        private_minio.make_bucket(bucket_name)
        private_minio.put_object(bucket_name, object_name, data, length)

        return True

    def save_screenshot_to_public_minio(self, url=None, bucket_name='mymymymymy', object_name=None):

        if not object_name:
            timestamp = str(datetime.datetime.now().isoformat()).replace(':', '_')
            object_name = 'screenshot-{}.png'.format(timestamp)
        else:
            object_name = 'screenshot.png'

        if url:
            self.browser.get(url)
            sleeper.seconds('Loading page', 4)

        png = self.browser.get_screenshot_as_png()

        bucket_name = bucket_name
        object_name = object_name
        data = io.BytesIO(png)
        length = data.getvalue().__len__()

        public_minio = use_public_server()
        public_minio.make_bucket(bucket_name)
        public_minio.put_object(bucket_name, object_name, data, length)

        return True

    def save_screenshot_to_file(self, url=None, object_name=None):

        if not object_name:
            timestamp = str(datetime.datetime.now().isoformat()).replace(':', '_')
            object_name = 'screenshot-{}.png'.format(timestamp)
        else:
            object_name = 'screenshot.png'

        if url:
            self.browser.get(url)
            sleeper.seconds('Loading page', 4)

        path = os.path.abspath('/tmp/hev')
        if not os.path.exists(path):
            os.makedirs(path)
        self.browser.save_screenshot(os.path.join(path, object_name))

        return True

    def new_resolution(self, width=1920, height=1080, device_type='web'):

        if device_type == 'pixel3':
            width = 1080
            height = 2160

        if device_type == 'web-small' or device_type == '800x600':
            width = 800
            height = 600

        if device_type == 'web-small-2' or device_type == '1024x768':
            width = 1024
            height = 768

        if device_type == 'web-small-3' or device_type == '1280x960':
            width = 1280
            height = 960

        if device_type == 'web-small-4' or device_type == '1280x1024':
            width = 1280
            height = 1024

        if device_type == 'web' or device_type == '1920x1080':
            width = 1920
            height = 1080

        if device_type == 'web-2' or device_type == '1600x1200':
            width = 1600
            height = 1200

        if device_type == 'web-3' or device_type == '1920x1200':
            width = 1920
            height = 1200

        if device_type == 'web-large' or device_type == '2560x1400':
            width = 2560
            height = 1400

        if device_type == 'web-long' or device_type == '1920x3080':
            width = 1920
            height = 3080

        self.browser.set_window_size(width, height)

    def quit(self):
        self.browser.close()
        self.browser.quit()
        self.browser.stop_client()


def click(browser, xpath):
    """Given an xpath, it will click it

    :param browser: selenium browser
    :param xpath: chrome xpath
    :return:
    """
    element = browser.find_element_by_xpath(xpath)
    return element.click()


def type(browser, keys):
    """Given a browser and a list of keys to perform

    :param browser: browser
    :param keys: list of keys
    :return: perform list of keys
    """
    actions = ActionChains(browser)
    for key in keys:
        actions.send_keys(key)

    return actions.perform()


def chrome():
    """Chrome with no options

    """
    warnings.warn('Docker does not support sandbox option')
    warnings.warn('Default shm size is 64m, which will cause chrome driver to crash.', Warning)

    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)


def chrome_sandboxed():
    """Chrome with sandbox enabled

    """
    warnings.warn('Docker does not support sandbox option')
    warnings.warn('Default shm size is 64m, which will cause chrome driver to crash.', Warning)

    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)


def chrome_headless_sandboxed():
    """Headless Chrome with sandbox enabled

    """
    warnings.warn('Docker does not support sandbox option')
    warnings.warn('Default shm size is 64m, which will cause chrome driver to crash.', Warning)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(options=options)


def chrome_headless_nosandbox():
    """Headless Chrome with sandbox disabled

    """
    warnings.warn('Default shm size is 64m, which will cause chrome driver to crash.', Warning)
    warnings.warn('''Possible error: <Future at 0x7f2504d09250 state=finished raised TimeoutException> Message: timeout
(Session info: headless chrome=75.0.3770.142)
''', Warning)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)


def chrome_headless_nosandbox_noshm():
    """Headless Chrome with sandbox disabled

    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


def chrome_headless_nosandbox_bigshm():
    """Headless Chrome with sandbox disabled

    """
    warnings.warn('Larger shm option is not implemented', Warning)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)


def chrome_remote(host='127.0.0.1', port='4444', executor_path='/wd/hub'):
    """Remote Selenium

    """
    hevlog.logging.info(
        'Remote WebDriver Hub URL: http://{}:{}{}/static/resource/hub.html'.format(host, port, executor_path))
    return webdriver.Remote(
        command_executor='http://{}:{}{}'.format(host, port, executor_path),
        desired_capabilities=DesiredCapabilities.CHROME
    )


if __name__ == "__main__":
    browser = chrome()
    browser.close()
    browser.quit()
