import unittest
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.websites_dev_page import WebsitesDevPage
from src.helpers.utilities import Utilities, UtilNoDriver
from selenium import webdriver


class DeletePageFromGrid(unittest.TestCase):
    # def setUp(self):
    #    self.driver = webdriver.Chrome()
    #    self.driver.maximize_window()

    def test_delete_page_from_grid(self, url=strings.localhost_solodev_url, username=strings.username,
                            password=strings.password, browser_type=strings.default_browser_type,
                            website_url=strings.sanity_page_url):
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
        websites_dev_page.click_folder("www")

        iframe_A = self.driver.find_element_by_css_selector("#multitabs_info_2")
        self.driver.switch_to.frame(iframe_A)

        # TODO Add page named 0-delete.stml so we always know the file name
        # TODO And it'll always be at the top of the list

        self.driver.find_element_by_css_selector('data-name="Add Page"').click()




    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

