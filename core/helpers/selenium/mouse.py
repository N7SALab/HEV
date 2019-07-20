def click(browser, xpath):
    """Given an xpath, it will click it

    :param browser: selenium browser
    :param xpath: chrome xpath
    :return:
    """
    browser = browser.find_element_by_xpath(xpath)
    return browser.click()
