import unittest

from src.helpers.utilities import UtilNoDriver
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from selenium import webdriver


class LoginTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_login(self, url, username, password, browser_type):
        """
        A simple login test

        Args
        :param    url: url to navigate to
        :param    username: solodev username
        :param    password: solodev password
        :param    browser_type: the browser to run the test against (Chrome, Firefox, etc) (case sensitive)
        """

        util_no_driver = UtilNoDriver(self)
        self.driver = util_no_driver.make_driver(browser_type, url)

        # Define webdriver wait and first page
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)

        # Go to the login page
        self.driver.get(url)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        login_page.type_login(username, password)
        login_page.click_login()

        # Log out
        home_page.click_profile()
        home_page.click_logout()

        # Assert we're back on login page
        self.assertTrue(login_page.login_button_present())
        self.driver.quit()

    def tearDown(self):
        # self.driver.quit()
        pass


# Required for unittest
if __name__ == "__main__":
    unittest.main()

