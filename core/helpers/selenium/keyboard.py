from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def type(browser, keys):
    """Given a browser and a list of keys to perform

    :param browser: browser
    :param keys: list of keys
    :return: perform list of keys
    """
    actions = ActionChains(browser)
    for key in keys:
        actions.send_keys(key)

    actions.perform()
