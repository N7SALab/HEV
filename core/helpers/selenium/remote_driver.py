from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from core.helpers.log import hevlog

hevlog = hevlog('selenium', level='debug')


def chrome_no_opt():
    """Chrome with no options

    """
    return webdriver.Chrome()


def chrome_headless_sandbox_enabled():
    """Headless Chrome with sandbox enabled

    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(options=options)


def chrome_headless_sandbox_disabled():
    """Headless Chrome with sandbox disabled

    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)


def chrome_remote(host='127.0.0.1', port='4444', executor_path='/wd/hub'):
    """Remote Selenium

    """
    hevlog.logging.info('Remote WebDriver Hub URL: http://{}:{}{}/static/resource/hub.html'.format(host, port, executor_path))
    return webdriver.Remote(
        command_executor='http://{}:{}{}'.format(host, port, executor_path),
        desired_capabilities=DesiredCapabilities.CHROME
    )
