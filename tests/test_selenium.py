from core.helpers.selenium import (mouse, keyboard)
from core.helpers.selenium.browser import (chrome_headless_sandbox_disabled, chrome_headless_sandbox_enabled,
                                           chrome_no_opt, chrome_sandbox_enabled, chrome_remote)


def test_chrome_headless_sandbox_disabled():
    chrome_headless_sandbox_disabled()


def disabled_test_chrome_headless_sandbox_enabled():
    assert chrome_headless_sandbox_enabled()


def disabled_test_chrome_no_opt():
    assert chrome_no_opt()


def disabled_test_chrome_sandbox_enabled():
    assert chrome_sandbox_enabled()


def disabled_test_chrome_remote():
    chrome_remote()
