import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from core.helpers.log import hevlog
from core.helpers.sleep import sleeper
from core.helpers.selenium.remote_driver import (chrome_headless_sandbox_disabled, chrome_headless_sandbox_enabled,
                                                 chrome_no_opt, chrome_remote)

hevlog = hevlog('instagram', level='debug')


def authenticate(username, password):
    """ Authenticates through browser and returns browser driver

    """

    # TODO: create capture proxy
    #       send traffic to /api
    login_page = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

    # browser = chrome_no_opt()
    browser = chrome_headless_sandbox_enabled()
    # browser = chrome_headless_sandbox_disabled()
    # browser = chrome_remote()

    browser.get(login_page)

    hevlog.logging.debug('[authenticating] {}'.format(login_page))

    sleeper.seconds('instagram get page', 1)

    actions = ActionChains(browser)
    actions.send_keys(Keys.TAB)
    actions.send_keys(username)
    actions.perform()

    # the password field is sometimes div[3] and div[4]
    login_pass_xpaths = [
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input',
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/div/label/input'
    ]

    for xpath in login_pass_xpaths:
        try:
            login_pass = browser.find_element_by_xpath(xpath)
            break
        except:
            pass

    login_btn = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')

    login_pass.send_keys(password)
    login_btn.click()

    sleeper.seconds('wait for instagram to log in', 2)
    hevlog.logging.debug(
        '[authenticated browser] [{}] {} session: {}'.format(browser.name, browser.title, browser.session_id))

    return browser


def get_stories(authenticated_browser, account):
    """ Retrieve story
    """
    story = 'https://www.instagram.com/stories/{}/'.format(account)
    stories = 0
    # TODO: set browser to redirect to proxy here
    # TODO: check if account exists
    browser = authenticated_browser
    browser.get(story)
    hevlog.logging.debug('[get stories] {}'.format(story))

    if 'Page Not Found' in browser.title:
        return stories

    sleeper.seconds('instagram', 1)

    while True:
        try:
            next = next_story(browser)
            stories += 1
        except:
            # TODO: disable browser proxy when done
            hevlog.logging.info('[get stories] done: {}'.format(account))
            return stories


def next_story(authenticated_browser):
    """ Click next story button
    """
    button = '//*[@id="react-root"]/section/div/div/section/div[2]/button[2]'
    browser = authenticated_browser.find_element_by_xpath(button)
    return browser.click()


def get_page(authenticated_browser, account):
    """ Get page
    """
    # TODO: need to download page
    page = 'https://instagram.com/{}'.format(account)
    b = authenticated_browser
    return b.get(page)


def run(instagram_config):
    login = instagram_config['login']['account']
    password = instagram_config['login']['password']
    accounts = instagram_config['following']

    hevlog.logging.debug('[login] {}'.format(login))
    hevlog.logging.debug('[accounts] {}'.format(len(accounts)))

    while True:
        if len(accounts) > 0:
            auth = authenticate(login, password)
            for account in accounts:
                hevlog.logging.info('[authenticated browser] [{}] {} session: {}'.format(auth.name, auth.title, auth.session_id))

                s = get_stories(auth, account)

                hevlog.logging.info('[{}] {} stories'.format(account, s))

        sleeper.hour('instagram')


def test_run(instagram_config):
    login = instagram_config['login']['account']
    password = instagram_config['login']['password']
    accounts = instagram_config['following']

    hevlog.logging.debug('[login] {}'.format(login))
    hevlog.logging.debug('[accounts] {}'.format(len(accounts)))

    if len(accounts) > 0:
        auth = authenticate(login, password)
        for account in accounts:
            hevlog.logging.info('[authenticated browser] [{}] {} session: {}'.format(auth.name, auth.title, auth.session_id))

            s = get_stories(auth, account)

            hevlog.logging.info('[{}] {} stories'.format(account, s))

            # just try one account so it tests faster
            break


if __name__ is '__main__':
    CONF = json.load(open('../../hev.conf'))
    run(CONF['instagram'])
