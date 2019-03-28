import unittest
import os
import time
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from selenium import webdriver

class AddLunarTemplate(unittest.TestCase):

    def __init__(self):
        self.driver = webdriver

    def test(self, url, username, password, website_url):
        desired_cap = {
        'browser': 'Chrome',
        'browser_version': '70.0',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '2048x1536'
        }

        self.url = url
        self.username = username
        self.password = password
        self.website_url = website_url

        self.driver = webdriver.Remote(
            command_executor= os.getenv("COMMAND_EXECUTOR"),
            desired_capabilities=desired_cap)
        self.driver.maximize_window()

        # Define webdriver wait and first page
        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)

        time.sleep(5)
        self.driver.get(AddLunarTemplate.url)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        login_page.type_login(AddLunarTemplate.username, AddLunarTemplate.password)
        login_page.click_login()

        # Create new website
        home_page.click_websites()

        websites_page.click_add_website()
        manage_website_page.type_website_url(self.website_url)
        manage_website_page.click_next()

        manage_website_page.click_lunar_xp()
        manage_website_page.click_next()

        utilities.wait_for_page_complete(30)

        manage_website_page.click_next()

        utilities.wait_for_page_complete(120)

        home_page = HomePage(self.driver)
        home_page.click_websites()
        websites_page.find_site_name(self.website_url)

        #self.driver.switch_to.default_content()

        home_page = HomePage(self.driver)
        utilities.wait_for_page_complete(1)
        home_page.click_profile()
        utilities.wait_for_page_complete(1)
        home_page.click_logout()

        # Assert we're back on login page
        self.assertTrue(login_page.login_button_present())

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    AddLunarTemplate.url = os.environ.get("URL", AddLunarTemplate.url)
    AddLunarTemplate.username = os.environ.get("USERNAME", AddLunarTemplate.username)
    AddLunarTemplate.password = os.environ.get("PASSWORD", AddLunarTemplate.password)
    AddLunarTemplate.new_page_url = os.environ.get("NEW_PAGE_URL", AddLunarTemplate.new_page_url)
    unittest.main()
