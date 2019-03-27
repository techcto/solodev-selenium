import unittest
from values import strings
from pageobjects.login_page import LoginPage
from pageobjects.home_page import HomePage
from pageobjects.websites_page import WebsitePage
from pageobjects.manage_website_page import ManageWebsitePage
from helpers.utilities import Utilities
from selenium import webdriver


class AddBlankPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    # All tests must start with _test
    # url, user, pass must be included for login
    def test_add_blank_page(self, url=strings.localhost_solodev_url,
                            username=strings.username, password=strings.password,
                            blank_page_name=strings.blank_page_name, current_website=strings.sanity_page_url):
        # Get the helper and page functions
        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)

        # Go to the login page
        self.driver.get(url)

        # Make sure it loads
        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        login_page.type_login(username, password)
        login_page.click_login()

