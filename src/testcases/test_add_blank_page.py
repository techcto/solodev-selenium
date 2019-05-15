import unittest
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.websites_dev_page import WebsitesDevPage
from src.helpers.utilities import Utilities, UtilNoDriver
from selenium import webdriver


class AddBlankPage(unittest.TestCase):
    # def setUp(self):
    #    self.driver = webdriver.Chrome()
    #    self.driver.maximize_window()

    def test_add_blank_page(self, url, username, password, browser_type, website_url):
        """
        This test adds a blank page to an existing website, either using the environment variable from the lambda
        function

        Args
        :param    url: url to navigate to
        :param    username: solodev username
        :param    password: solodev password
        :param    website_url: url to be the name of the site we are adding to the cms
        :param    browser_type: the browser to run the test against (Chrome, Firefox, etc) (case sensitive)
        """

        util_no_driver = UtilNoDriver(self)
        self.driver = util_no_driver.make_driver(browser_type, url)

        # Get the helper and page functions
        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        websites_dev_page = WebsitesDevPage(self.driver)

        # Go to the login page
        self.driver.get(url)

        # Make sure it loads
        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        login_page.type_login(username, password)
        login_page.click_login()

        # click into the website
        home_page.click_websites()
        home_page.click_a_website(website_url)

        # expand web files
        websites_dev_page.expand_folder("www")
        websites_dev_page.click_folder("about")

        # This test is incomplete
        # TODO this test should add the page 0-delete.stml mentioned in the delete page tests
        # TODO this test should then be run before each of the delete tests

    def tearDown(self):
        self.driver.quit()


# Required for unittest
if __name__ == "__main__":
    unittest.main()

