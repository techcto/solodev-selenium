import unittest
import os
import time
import json
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from src.pageobjects.websites_dev_page import WebsitesDevPage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class AddLunarTemplate(unittest.TestCase):
    # url = ""
    # username = ""
    # password = ""
    # website_url = ""

    # def setUp(self):
    #    self.driver = webdriver

    def test_90second_website_launch(self, url=strings.localhost_solodev_url,
                                     username=strings.username, password=strings.password,
                                     website_url=strings.sanity_page_url):
        desired_cap = {
            'browser': 'Firefox',
            'browser_version': '66.0',
            'os': 'Windows',
            'os_version': '10',
            'resolution': '1920x1080',
            'browserstack.console': 'verbose',
            'browserstack.selenium_version': '3.14.0'
        }

        self.url = url
        self.username = username
        self.password = password
        self.website_url = website_url
        self.driver = webdriver

        if "localhost" in url:
            #self.driver = webdriver.Chrome()
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Remote(
                command_executor=os.getenv("COMMAND_EXECUTOR"),
                desired_capabilities=desired_cap)

        self.driver.fullscreen_window()

        # Define webdriver wait and first page
        # utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)
        # websites_dev_page = WebsitesDevPage(self.driver)

        time.sleep(10)
        self.driver.get(self.url)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        time.sleep(5)
        login_page.type_login(self.username, self.password)
        login_page.click_login()

        # Create new website
        home_page.click_websites()

        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Add Website")))

        websites_page.click_add_website()
        manage_website_page.type_website_url(self.website_url)
        manage_website_page.click_next()

        manage_website_page.click_lunar_xp()
        manage_website_page.click_next()

        wait.until(ec.presence_of_element_located((By.ID, "appForm")))
        self.driver.set_page_load_timeout(10)

        try:
            manage_website_page.click_next()
        except TimeoutException:
            print("caught exception, checking for if page is ready")
            # print(e.stacktrace)
            pass

        wait = WebDriverWait(self.driver, 600)
        wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Start Managing Your Website")))

        manage_website_page = ManageWebsitePage(self.driver)
        manage_website_page.click_start_managing()

        websites_dev_page = WebsitesDevPage(self.driver)
        #websites_dev_page.find_site_name()

        websites_dev_page.expand_folder("www")
        websites_dev_page.click_page("index.stml")

        #Open new tab
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
        self.driver.get(website_url)

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


if __name__ == "__main__":
    unittest.main()

