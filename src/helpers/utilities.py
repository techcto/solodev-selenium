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
        """
        When using a page load strategy other than 'normal', we manually need to tell the test to wait
        after each page event, so this method was created. It checks to see if the page status is
        'complete' by default. See the use in the 90 second website launch test

        :param driver: the webdriver
        :param states: javascript page status: complete, loading, interactive, etc
        :param pending: TODO
        :return:
        """
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
        """
        Wait until the item at locator is visible using wait.until presence of element
        :param driver: webdriver
        :param timeout: timeout in seconds to wait for locator
        :param locator: type webelement
        :return:
        """
        wait = WebDriverWait(driver, timeout)
        wait.until(ec.presence_of_element_located(locator))
        return True

    # returns true if there are elements that match the selector
    # returns false of there are no elements that match the selector
    # locater = xpath to element = "//td[contains(text(), 'some element text')]" for example
    def presence_of_elements_by_xpath(self, driver, locator):
        present = len(driver.find_elements_by_xpath(locator)) > 0
        if present > 0:
            return True
        else:
            return False

    # returns true if there are elements that match the selector
    # returns false of there are no elements that match the selector
    # locater = xpath to element = '[aria-label="Log Out"]' for example
    def presence_of_elements_by_css_selector(self, driver, locator):
        present = len(driver.find_elements_by_css_selector(locator)) > 0
        if present > 0:
            return True
        else:
            return False


# page load strategy should be normal 99% of the time
# the only time it shouldnt is when chrome needs to load a long page and we need to trick browserstack
# if set to none, you need to use wait for page complete method above after
# every command that would change the page (clicking links, buttons, etc)
class UtilNoDriver(BasePage):
    def make_driver(self, browser_type, url, page_load_strategy="normal"):
        """
        Because the capabilities the webdriver needs for development vs local vs browserstack differ so much
        we need a function to handle this for us.

        Args
        :param browser_type: Chrome/Firefox/Edge/IE/Safari
        :param url: the url to navigate to
        :param page_load_strategy: defaults to normal, read more here
        https://stackoverflow.com/questions/43734797/page-load-strategy-for-chrome-driver-updated-till-selenium-v3-12-0
        :return:
        """
        desired_cap = {
            'acceptSslCerts ': 'true',
            'os': 'Windows',
            'os_version': '10',
            'resolution': '1920x1080',
            'browserstack.console': 'verbose',
            'browserstack.selenium_version': '3.14.0'
        }

        # For both browser types, the browser version is hard coded.
        # Eventually this will need to be updated at the same time the webdriver is
        if "Chrome" in browser_type:
            desired_cap['pageLoadStrategy'] = page_load_strategy
            desired_cap['browser'] = browser_type,
            desired_cap['browser_version'] = '70.0',
            if "localhost" in url:
                self.driver = webdriver.Chrome(desired_capabilities=desired_cap)
                self.driver.maximize_window()
                time.sleep(10)
            else:
                self.driver = webdriver.Remote(
                    command_executor=os.getenv("COMMAND_EXECUTOR"),
                    desired_capabilities=desired_cap)
                self.driver.fullscreen_window()
                time.sleep(60)
        elif "Firefox" in browser_type:
            desired_cap['pageLoadStrategy'] = page_load_strategy
            desired_cap['browser'] = browser_type,
            desired_cap['browser_version'] = '66.0',
            if "localhost" in url:
                self.driver = webdriver.Firefox(desired_capabilities=desired_cap)
                self.driver.maximize_window()
                time.sleep(10)
            else:
                self.driver = webdriver.Remote(
                    command_executor=os.getenv("COMMAND_EXECUTOR"),
                    desired_capabilities=desired_cap)
                self.driver.fullscreen_window()
                time.sleep(60)

        return self.driver

