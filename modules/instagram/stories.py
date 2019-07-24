from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from core.helpers.log import hevlog
from core.helpers.sleep import sleeper
from core.helpers.selenium.browser import (Browser, chrome_nosandbox, chrome_headless_nosandbox,
                                           chrome, chrome_for_docker, chrome_headless_nosandbox_bigshm,
                                           chrome_headless_nosandbox_noshm, chrome_headless_nosandbox_unsafe,
                                           chrome_headless_sandboxed, chrome_remote, chrome_sandboxed,
                                           click, type)

from core.helpers import minio

hevlog = hevlog('instagram', level='debug')


def authenticate(username, password, minio_client=None, retries=None):
    """Authenticates through browser and returns browser driver

    :param username: username string
    :param password: password string
    :param retries: not implemented
    :return: authenticated browser
    """

    while True:

        # TODO: create capture proxy
        #       send traffic to /api
        login_page = 'https://www.instagram.com/accounts/login/?source=auth_switcher'

        # browser = Browser(chrome())
        # browser = Browser(chrome_headless_nosandbox())
        browser = Browser(chrome_for_docker())
        # browser = Browser(chrome_sandboxed())
        # browser = Browser(chrome_headless_sandboxed())
        # browser = Browser(chrome_remote())

        if minio_client:
            browser.set_minio_client(minio_client)

        browser.browser.get(login_page)

        browser.save_screenshot_to_minio()

        hevlog.logging.debug('[authenticate] {}'.format(login_page))

        sleeper.seconds('instagram get page', 1)

        actions = ActionChains(browser.browser)
        actions.send_keys(Keys.TAB)
        actions.send_keys(username)
        actions.perform()

        sleeper.seconds('instagram get page', 1)

        # the password field is sometimes div[3] and div[4]
        login_pass_xpaths = [
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input',
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/div/label/input'
        ]

        login_btn_xpaths = [
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button',
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[6]/button'
        ]

        found_pass = False
        for xpath in login_pass_xpaths:
            try:
                login_pass = browser.browser.find_element_by_xpath(xpath)
                found_pass = True
                break
            except:
                pass

        sleeper.seconds('instagram get page', 2)

        found_btn = False
        for xpath in login_btn_xpaths:
            try:
                login_btn = browser.browser.find_element_by_xpath(xpath)
                found_btn = True
                break
            except:
                pass

        if found_pass and found_btn:
            break
        else:
            hevlog.logging.error('[browser] Authentication failed')

            hevlog.logging.debug(
                '[browser] Found password field: {} Found login button: {}'.format(browser.browser.name, found_pass,
                                                                                   found_btn))

            sleeper.minute("instagram can't authenticate")

    login_pass.send_keys(password)
    login_btn.click()

    sleeper.seconds('wait for instagram to log in', 5)

    hevlog.logging.debug(
        '[authenticated browser] [{}] {} session: {}'.format(browser.browser.name, browser.browser.title,
                                                             browser.browser.session_id))
    browser.save_screenshot_to_minio()

    return browser


def get_stories(authenticated_browser, account):
    """ Retrieve story
    """
    story = 'https://www.instagram.com/stories/{}/'.format(account)
    num_of_stories = 0
    # TODO: set browser to redirect to proxy here
    # TODO: check if account exists
    browser = authenticated_browser

    browser.browser.get(story)

    hevlog.logging.debug('[get stories] {}'.format(story))

    if 'Page Not Found' in browser.browser.title:
        hevlog.logging.debug('[get_stories] no stories for {}'.format(account))
        return num_of_stories

    sleeper.seconds('instagram', 2)

    while True:
        try:
            next_story(browser)

            title = browser.browser.title
            if title == 'Instagram':
                hevlog.logging.debug(('[get_stories] {} end of stories'.format(account)))
                raise Exception
            num_of_stories += 1
            sleeper.seconds('watch the story for a bit', 1)
            browser.save_screenshot_to_minio()
        except:
            # TODO: disable browser proxy when done
            hevlog.logging.debug('[get stories] done: {}'.format(account))
            return num_of_stories


def next_story(authenticated_browser):
    """ Click next story button
    """

    xpaths = [
        '//*[@id="react-root"]/section/div/div/section/div[2]/div[1]/div/div/div[2]/div/div/button',
        '//*[@id="react-root"]/section/div/div/section/div[2]/button[2]'
    ]

    found_btn = False
    for xpath in xpaths:
        try:
            browser = authenticated_browser
            button = browser.browser.find_element_by_xpath(xpath)
            found_btn = True
            hevlog.logging.debug('[next_story] next story')
            return button.click()
        except:
            pass

    if not found_btn:
        # no more stories. exit
        hevlog.logging.debug('[next_story] no more stories')
        raise Exception


def get_page(authenticated_browser, account):
    """ Get page
    """
    # TODO: need to download page
    hevlog.logging.debug('[get_page] getting {}'.format(account))
    page = 'https://instagram.com/{}'.format(account)
    browser = authenticated_browser
    return browser.browser.get(page)


def run(config):
    client = minio.client(config['minio-hev'], secure=False)

    instagram_config = config['instagram']
    login = instagram_config['login']['account']
    password = instagram_config['login']['password']
    accounts = instagram_config['following']

    hevlog.logging.debug('[login] {}'.format(login))
    hevlog.logging.info('Running...')
    hevlog.logging.info('[accounts] {}'.format(len(accounts)))

    while True:

        if len(accounts) > 0:

            browser = authenticate(login, password, client)

            for account in accounts:

                while True:
                    if runrun(browser, account):
                        break
                    else:
                        browser = authenticate(login, password, client)

        sleeper.hour('instagram')


def runrun(browser, account):
    hevlog.logging.debug(
        '[runrun] [{}] {} session: {}'.format(browser.browser.name, browser.browser.title,
                                              browser.browser.session_id))

    num_of_stories = get_stories(browser, account)

    hevlog.logging.info('[{}] {} stories'.format(account, num_of_stories))

    # sleeper.minute('instagram')

    return True


def test_run(config):
    client = minio.client(config['minio-hev'], secure=False)

    instagram_config = config['instagram']
    login = instagram_config['login']['account']
    password = instagram_config['login']['password']
    accounts = instagram_config['following']

    hevlog.logging.debug('[login] {}'.format(login))
    hevlog.logging.info('Running...')
    hevlog.logging.info('[accounts] {}'.format(len(accounts)))

    while True:

        if len(accounts) > 0:

            browser = authenticate(login, password, client)

            for account in accounts:

                while True:
                    if runrun(browser, account):
                        break
                    else:
                        browser = authenticate(login, password, client)

                    return
