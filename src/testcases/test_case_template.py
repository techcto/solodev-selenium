import unittest
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from src.helpers.utilities import UtilNoDriver
from selenium import webdriver


class TestCaseTemplate(unittest.TestCase):
    """
    This template isn't designed to be run, but to serve as a template for developers to create additional tests
    """

    def setUp(self):
        """
        This is where the driver setup _should_ go, but lambda/browserstack doesn't like it
        I don't think Lambda is aware of unit tests or test suites in general
        Which will break pretty test result reporting in browserstack
        """
        self.driver = webdriver.Chrome()

    # All tests must start with _test
    # url, user, pass must be included for login
    def test_case_template(self, url=strings.localhost_solodev_url,
                                     username=strings.username, password=strings.password,
                                     website_url=strings.sanity_page_url, browser_type=strings.default_browser_type):
        """
        Args
        :param    url: url to navigate to
        :param    username: solodev username
        :param    password: solodev password
        :param    website_url: url to be the name of the site we are adding to the cms
        :param    browser_type: the browser to run the test against (Chrome, Firefox, etc) (case sensitive)
        """

        # We have to declare the driver first
        # It has to have browser type (firefox/chrome supported now)
        # the URL to know if we're running aginst local or aws
        # the "page load strategy" which defaults to "normal", so you con't actually need to put normal
        util_no_driver = UtilNoDriver(self)
        self.driver = util_no_driver.make_driver(browser_type, url, "normal")

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

        # Assert true - some element is or isn't there, or some function that returns T/F
        # The driver.quit is here for a safeguard, it shouldn't ever be called,
        # But its unclear if browserstack obeys assert's properly
        # This assert example makes sure the element is present by checking a list of matching elements is > 0
        self.assertTrue(len(self.driver.find_elements_by_css_selector(".btn.btn-lg.btn-yellow")) > 0)

        # this driver quit inside the test shouldn't be necessary once the
        # browserstack / lambda function interaction is figured out
        self.driver.quit()

    # this should quit the driver properly after the assertion
    def tearDown(self):
        self.driver.quit()

# Required for unittest
if __name__ == "__main__":
    unittest.main()