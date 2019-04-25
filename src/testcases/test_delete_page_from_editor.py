import unittest
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.websites_dev_page import WebsitesDevPage
from src.helpers.utilities import Utilities, UtilNoDriver
from selenium import webdriver


class DeletePageFromEditor(unittest.TestCase):
    # def setUp(self):
    #    self.driver = webdriver.Chrome()
    #    self.driver.maximize_window()

    def test_delete_page_from_editor(self, url=strings.localhost_solodev_url, username=strings.username,
                            password=strings.password, browser_type=strings.default_browser_type,
                            website_url=strings.sanity_page_url):

        """
        This delete test navigates to the page editor, and clicks the delete icon on the top of the page

        Args
        :param    url: url to navigate to
        :param    username: solodev username
        :param    password: solodev password
        :param    website_url: url to be the name of the site we are adding to the cms
        :param    browser_type: the browser to run the test against (Chrome, Firefox, etc) (case sensitive)
        :return:
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
        # TODO Add page named 0-delete.stml so we always know the file name
        # TODO And it'll always be at the top of the list
        websites_dev_page.click_page("404.stml")

        # delete page clicked above
        iframe_A = self.driver.find_element_by_css_selector("#multitabs_info_2")
        self.driver.switch_to.frame(iframe_A)

        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-trash']")
        delete.click()

        self.driver.switch_to.parent_frame()

        # action_modal = self.driver.find_element_by_css_selector("#actionModal")
        self.driver.find_element_by_css_selector(
            "#actionModalForm > div > .modal-content > div > .btn.btn-color1.btn-lg.modal-confirm").click()

        # This test is incomplete

    def tearDown(self):
        self.driver.quit()


# Required for unittest
if __name__ == "__main__":
    unittest.main()


