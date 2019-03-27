import unittest
import time
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from selenium import webdriver


class SanityTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_sanity(self, url=strings.localhost_solodev_url,
                    username=strings.username, password=strings.password, new_page_url=strings.sanity_page_url):
        # Define webdriver wait and first page
        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)

        self.driver.get(url)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        login_page.type_login(username, password)
        login_page.click_login()

        # Create new website
        home_page.click_websites()

        websites_page.click_add_website()
        manage_website_page.type_website_url(new_page_url)
        manage_website_page.click_next()

        manage_website_page.click_lunar_xp()
        manage_website_page.click_next()

        utilities.wait_for_page_complete(30)

        manage_website_page.click_next()

        utilities.wait_for_page_complete(120)

        # We should have a website now... so lets delete it!
        home_page = HomePage(self.driver)
        home_page.click_websites()
        websites_page.click_site_name(new_page_url)

        # Click settings button
        iframe_A = self.driver.find_element_by_css_selector("#multitabs_info_1")
        self.driver.switch_to.frame(iframe_A)
        utilities.wait_for_page_complete(1)
        manage_website_page.click_settings()
        self.driver.switch_to.default_content()

        # Expand advanced tab
        iframe_B = self.driver.find_element_by_css_selector("#actionFrame")
        self.driver.switch_to.frame(iframe_B)
        utilities.wait_for_page_complete(1)
        manage_website_page = ManageWebsitePage(self.driver)
        manage_website_page.toggle_advanced()

        # Delete the site
        manage_website_page = ManageWebsitePage(self.driver)
        manage_website_page.delete_site()
        # Sleeping in a test like this sucks, but the page thinks its "complete" when deleting.
        # Maybe change page behavior, so its more like adding a site?
        time.sleep(10)
        utilities.wait_for_page_complete(5)
        self.driver.switch_to.default_content()

        # Todo check if website name is anywhere on the page. if not, continue, if so, fail
        if utilities.presence_of_elements_by_xpath(self.driver, "//td[contains(text(), '"
                                                                + strings.sanity_page_url + "')]"):
            self.assertTrue(False)

        # Log out
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
    unittest.main()

