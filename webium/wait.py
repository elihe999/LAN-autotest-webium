import webium.settings
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from waiting import wait as wait_lib
from webium.driver import get_driver


def wait(*args, **kwargs):
    """
    Wrapping 'wait()' method of 'waiting' library with default parameter values.
    WebDriverException is ignored in the expected exceptions by default.
    """
    kwargs.setdefault('sleep_seconds', (1, None))
    kwargs.setdefault('expected_exceptions', WebDriverException)
    kwargs.setdefault('timeout_seconds', webium.settings.wait_timeout)

    return wait_lib(*args, **kwargs)

def webiumLongWait():
    return WebDriverWait(get_driver(), webium.settings.longwaitnum)

def webiumMiddleWait():
    return WebDriverWait(get_driver(), webium.settings.middlewaitnum)

def webiumShortWait():
    return WebDriverWait(get_driver(), webium.settings.shortwaitnum)

def webiumWait():
    return WebDriverWait(get_driver(), webium.settings.waitnum)
