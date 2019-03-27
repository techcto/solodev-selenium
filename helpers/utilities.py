from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver


class Utilities(BasePage):
    def wait_for_page_complete(self, timeout):
        self.driver.implicitly_wait(1)
        page_state = self.driver.execute_script('return document.readyState;')
        i = 0
        while not page_state == 'complete':
            self.driver.implicitly_wait(1)
            if i == timeout:
                break

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

