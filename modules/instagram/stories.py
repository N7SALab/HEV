import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from core.helpers.log import hevlog
from core.helpers.sleep import sleeper

hevlog = hevlog('instagram', level='debug')


def authenticate(username, password):
    """ Authenticates through browser and returns browser driver

    """

    # TODO: create capture proxy
    #       send traffic to /api
    login_page = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)
    # browser = webdriver.Chrome()
    browser.get(login_page)
    hevlog.logging.debug('[authenticating] {}'.format(login_page))
    sleeper.seconds('instagram authenticate', 1)

    actions = ActionChains(browser)
    actions.send_keys(Keys.TAB)
    actions.send_keys(username)
    actions.perform()

    login_pass = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/div[1]/input')
    login_btn = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button')

    login_pass.send_keys(password)
    login_btn.click()

    sleeper.seconds('instagram authenticate', 2)
    hevlog.logging.debug('[authenticated browser] [{}] {} {}'.format(browser.name, browser.title, browser.session_id))

    return browser


def get_stories(authenticated_browser, account):
    """ Retrieve story
    """
    story = 'https://www.instagram.com/stories/{}/'.format(account)
    stories = 1
    # TODO: set browser to redirect to proxy here
    # TODO: check if account exists
    browser = authenticated_browser
    browser.get(story)
    hevlog.logging.debug('[get stories] {}'.format(story))

    if 'Page Not Found' in browser.title:
        stories -= 1
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
    hevlog.logging.debug('[login] {}'.format(login))
    password = instagram_config['login']['password']

    accounts = instagram_config['following']
    hevlog.logging.debug('[accounts] {}'.format(len(accounts)))

    while True:
        if len(accounts) > 0:
            auth = authenticate(login, password)
            for account in accounts:
                hevlog.logging.info('[authenticated browser] [{}] {} {}'.format(auth.name, auth.title, auth.session_id))
                s = get_stories(auth, account)
                hevlog.logging.info('[{}] {} stories'.format(account, s))

        sleeper.hour('instagram')


if __name__ is '__main__':

    CONF = json.load(open('../../hev.conf'))
    run(CONF['instagram'])
