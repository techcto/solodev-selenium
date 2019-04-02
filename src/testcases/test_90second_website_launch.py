import unittest
import os
import time
import json
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from selenium import webdriver


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
            'browser': 'Chrome',
            'browser_version': '70.0',
            'os': 'Windows',
            'os_version': '10',
            'resolution': '1920x1080',
            'browserstack.console': 'verbose'
        }

        self.url = url
        self.username = username
        self.password = password
        self.website_url = website_url
        self.driver = webdriver

        if "localhost" in url:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Remote(
                command_executor=os.getenv("COMMAND_EXECUTOR"),
                desired_capabilities=desired_cap)

        self.driver.fullscreen_window()

        # Define webdriver wait and first page
        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)

        time.sleep(30)
        self.driver.get(self.url)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        time.sleep(5)
        login_page.type_login(self.username, self.password)
        login_page.click_login()

        # Create new website
        home_page.click_websites()

        websites_page.click_add_website()
        manage_website_page.type_website_url(self.website_url)
        manage_website_page.click_next()

        manage_website_page.click_lunar_xp()
        manage_website_page.click_next()

        # utilities.wait_for_page_complete(30)

        manage_website_page.click_next()

        # utilities.wait_for_page_complete(120)

        home_page = HomePage(self.driver)
        home_page.click_websites()
        websites_page.find_site_name(self.website_url)

        #self.driver.switch_to.default_content()

        home_page = HomePage(self.driver)
        # utilities.wait_for_page_complete(1)
        home_page.click_profile()
        # utilities.wait_for_page_complete(1)
        home_page.click_logout()

        # self.driver.get(self.website_url)
        self.driver.get("http://lunarxp.com")

        hold_key(self.driver, 4)

        # Assert we're at the bottom of the page
        self.assertTrue(len(self.driver.find_elements_by_css_selector(".btn.btn-lg.btn-yellow")) > 0)
        self.driver.quit()

    # def tearDown(self):
    #    self.driver.quit()


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

