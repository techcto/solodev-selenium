import os

import time
from enum import Enum
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class BrowserType(Enum):
    Chrome = 1
    Firefox = 2


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver


class Utilities(BasePage):
    def wait_for_page_complete(self, driver, states="complete", pending=None):
        print('> waiting...', end='', flush=True)
        while True:
            state = driver.execute_script('return document.readyState;')
            if state not in states:
                print('.', end='', flush=True)
                if callable(pending):
                    pending()
                time.sleep(1)
            else:
                break
        print('', state)
        # seems like once we hit the ready state the browser still needs just
        # a little more time
        time.sleep(3)

    def wait_until_visible(self, driver, timeout, locator):
        wait = WebDriverWait(driver, timeout)
        wait.until(ec.presence_of_element_located(locator))
        return True

    # returns true if there are elements that match the selector
    # returns false of there are no elements that match the selector
    # locater = xpath to element = "//td[contains(text(), 'some element text')]" for example
    def presence_of_elements_by_xpath(self, driver, locator):
        present = len(driver.find_elements_by_xpath(locator)) > 0
        return present

    # returns true if there are elements that match the selector
    # returns false of there are no elements that match the selector
    # locater = xpath to element = '[aria-label="Log Out"]' for example
    def presence_of_elements_by_css_selector(self, driver, locator):
        present = len(driver.find_elements_by_css_selector(locator)) > 0
        return present

# page load strategy should be normal 99% of the time
# the only time it shouldnt is when chrome needs to load a long page and we need to trick browserstack
# if set to none, you need to use wait for page complete method above after
# every command that would change the page (clicking links, buttons, etc)
class UtilNoDriver(BasePage):
    def make_driver(self, browser_type, url, page_load_strategy="normal"):
        desired_cap = {
            'browser': browser_type,
            'browser_version': '66.0',
            'acceptSslCerts ': 'true',
            'os': 'Windows',
            'os_version': '10',
            'resolution': '1920x1080',
            'browserstack.console': 'verbose',
            'browserstack.selenium_version': '3.14.0'
        }

        if "localhost" in url:
            if "Chrome" in browser_type:
                desired_cap['pageLoadStrategy'] = page_load_strategy
                self.driver = webdriver.Chrome(desired_capabilities=desired_cap)
            elif "Firefox" in browser_type:
                self.driver = webdriver.Firefox(desired_capabilities=desired_cap)
            self.driver.maximize_window()
        else:
            self.driver = webdriver.Remote(
                command_executor=os.getenv("COMMAND_EXECUTOR"),
                desired_capabilities=desired_cap)
            self.driver.fullscreen_window()

        return self.driver


