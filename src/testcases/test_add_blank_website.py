import datetime
import unittest
import time
import json
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from src.helpers.utilities import UtilNoDriver
from src.pageobjects.websites_dev_page import WebsitesDevPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class AddBlankWebsite(unittest.TestCase):
    # def setUp(self):
    #    self.driver = webdriver.Chrome()
    #    self.driver.maximize_window()

    def test_add_blank_website(self, url=strings.localhost_solodev_url,
                    username=strings.username, password=strings.password,
                    new_page_url=strings.sanity_page_url, browser_type=strings.default_browser_type):
        """
        This test adds a blank website, selecting no template when the deployment gets to that step

        Args
        :param    url: url to navigate to
        :param    username: solodev username
        :param    password: solodev password
        :param    website_url: url to be the name of the site we are adding to the cms
        :param    browser_type: the browser to run the test against (Chrome, Firefox, etc) (case sensitive)
        """

        util_no_driver = UtilNoDriver(self)
        self.driver = util_no_driver.make_driver(browser_type, url, "none")

        utilities = Utilities(self.driver)
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)
        websites_page = WebsitePage(self.driver)
        manage_website_page = ManageWebsitePage(self.driver)
        # websites_dev_page = WebsitesDevPage(self.driver)

        self.driver.get(url)
        utilities.wait_for_page_complete(self.driver)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        time.sleep(5)
        login_page.type_login(username, password)
        login_page.click_login()
        utilities.wait_for_page_complete(self.driver)

        # Create new website
        home_page.click_websites()
        utilities.wait_for_page_complete(self.driver)

        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Add Website")))
        websites_page.click_add_website()
        utilities.wait_for_page_complete(self.driver)

        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#name")))
        manage_website_page.type_website_url(new_page_url)
        manage_website_page.click_next()
        utilities.wait_for_page_complete(self.driver)

        manage_website_page.click_blank_website()
        utilities.wait_for_page_complete(self.driver)

        wait = WebDriverWait(self.driver, 1200)
        if "Firefox" in browser_type:
            self.driver.set_page_load_timeout(10)
            try:
                manage_website_page.click_next()
            except TimeoutException:
                print('NOTE: at this point we can do other browser things to keep browserstack happy')
                pass
            wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Start Managing Your Website")))
        elif "Chrome" in browser_type:
            manage_website_page.click_next()
            utilities.wait_for_page_complete(self.driver, states=("interactive", "complete"))
            print('NOTE: at this point we can do other browser things to keep browserstack happy')
            wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Start Managing Your Website")))

        manage_website_page = ManageWebsitePage(self.driver)
        manage_website_page.click_start_managing()
        utilities.wait_for_page_complete(self.driver)

        self.driver.switch_to.default_content()

        # Todo check if website name is anywhere on the page. if not, continue, if so, fail
        if utilities.presence_of_elements_by_xpath(self.driver, "//td[contains(text(), '"
                                                                + strings.sanity_page_url + "')]"):
            self.assertTrue(False)

        # Log out
        home_page = HomePage(self.driver)
        home_page.click_profile()
        utilities.wait_for_page_complete(self.driver)
        home_page.click_logout()
        utilities.wait_for_page_complete(self.driver)

        # Assert we're back on login page
        self.assertTrue(login_page.login_button_present())
        self.driver.quit()

    def tearDown(self):
        self.driver.quit()



# Required for unittest
if __name__ == "__main__":
    unittest.main()


