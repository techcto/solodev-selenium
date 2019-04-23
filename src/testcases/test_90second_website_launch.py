import datetime
import unittest
import time
import json
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from src.helpers.utilities import UtilNoDriver
from src.pageobjects.websites_dev_page import WebsitesDevPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class AddLunarTemplate(unittest.TestCase):
    
    # This is where the driver setup _should_ go, but lambda/browserstack doesn't like it
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_90second_website_launch(self, url=strings.localhost_solodev_url,
                                     username=strings.username, password=strings.password,
                                     website_url=strings.sanity_page_url, browser_type=strings.default_browser_type):

        util_no_driver = UtilNoDriver(self)
        self.driver = util_no_driver.make_driver(browser_type, url, "none")

        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)
        # websites_dev_page = WebsitesDevPage(self.driver)

        self.driver.get(url)
        utilities.wait_for_page_complete(self.driver)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        time.sleep(5)
        login_page.type_login(username, password)
        login_page.click_login()
        utilities.wait_for_page_complete(self.driver)

        # Create new website
        home_page.click_websites()
        utilities.wait_for_page_complete(self.driver)

        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Add Website")))
        websites_page.click_add_website()
        utilities.wait_for_page_complete(self.driver)

        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#name")))
        manage_website_page.type_website_url(website_url)
        manage_website_page.click_next()
        utilities.wait_for_page_complete(self.driver)

        manage_website_page.click_lunar_xp()
        utilities.wait_for_page_complete(self.driver)
        manage_website_page.click_next()
        utilities.wait_for_page_complete(self.driver)

        wait = WebDriverWait(self.driver, 1200)
        if "Firefox" in browser_type:
            self.driver.set_page_load_timeout(10)
            try:
                manage_website_page.click_next()
            except TimeoutException:
                print('NOTE: at this point we can do other browser things to keep browserstack happy')
                pass
            wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Start Managing Your Website")))
        elif "Chrome" in browser_type:
            manage_website_page.click_next()
            utilities.wait_for_page_complete(self.driver, states=("interactive", "complete"))
            print('NOTE: at this point we can do other browser things to keep browserstack happy')
            wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Start Managing Your Website")))

        manage_website_page = ManageWebsitePage(self.driver)
        manage_website_page.click_start_managing()
        utilities.wait_for_page_complete(self.driver)

        websites_dev_page = WebsitesDevPage(self.driver)
        # websites_dev_page.find_site_name()

        websites_dev_page.expand_folder("www")
        utilities.wait_for_page_complete(self.driver)
        websites_dev_page.click_page("index.stml")
        utilities.wait_for_page_complete(self.driver)

        # Open new tab
        # self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
        self.driver.get("http://lunarxp.com")
        utilities.wait_for_page_complete(self.driver)

        hold_key(self.driver, 4)

        # Assert we're at the bottom of the page
        self.assertTrue(len(self.driver.find_elements_by_css_selector(".btn.btn-lg.btn-yellow")) > 0)
        self.driver.quit()

    def tearDown(self):
        self.driver.quit()


def dispatch_key_event(driver, name, options={}):
    options["type"] = name
    body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
    resource = "/session/%s/chromium/send_command" % driver.session_id
    locator = driver.command_executor._url + resource
    driver.command_executor._request('POST', locator, body)


def hold_key(driver, duration):
    endtime = time.time() + duration
    options = {
        "type": "<TYPE>",
        "key": "ArrowDown",
        "code": "ArrowDown",
        "nativeVirtualKeyCode": 40,
        "windowsVirtualKeyCode": 40
    }

    while True:
        dispatch_key_event(driver, "rawKeyDown", options)
        dispatch_key_event(driver, "char", options)

        if time.time() > endtime:
            dispatch_key_event(driver, "keyUp", options)
            break

        options["autoRepeat"] = True
        time.sleep(0.01)


def click_element(driver, el):
    """Helper function for simulating button clicks while the browser is busy."""
    def func():
        actions = ActionChains(driver)
        actions.click(el)
        actions.perform()
    return func


if __name__ == "__main__":
    unittest.main()

