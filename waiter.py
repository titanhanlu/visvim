
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select

class options_more_than_one(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = _find_element(driver, self.locator)
        if len(Select(element).options) > 1:
            return element
        else:
            return False

def _find_element(driver, by):
    """Looks up an element. Logs and re-raises ``WebDriverException``
    if thrown."""
    try:
        return driver.find_element(*by)
    except NoSuchElementException as e:
        raise e
    except WebDriverException as e:
        raise e





