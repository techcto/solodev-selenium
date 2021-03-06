import unittest

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.pageobjects.websites_dev_page import WebsitesDevPage
from selenium.webdriver.support import expected_conditions as ec
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from src.pageobjects.websites_page import WebsitePage
from src.pageobjects.manage_website_page import ManageWebsitePage
from src.helpers.utilities import Utilities
from src.helpers.utilities import UtilNoDriver

class AddLunarTemplate(unittest.TestCase):
    g_url = None
    g_username = None
    g_password = None
    g_website_url = None
    g_browser_type = None

    def setUp(self):
        """
        This is where the driver setup _should_ go, but lambda/browserstack doesn't like it
        I don't think Lambda is aware of unit tests or test suites in general
        Which will break pretty test result reporting in browserstack
        """
        pass
        # self.driver = webdriver.Chrome()

    def test_add_lunar(self, url = None, username = None, password = None, website_url = None, browser_type = None):
        # NOTE: test cases that are executed by the unittest runner don't have parameters passed to their
        # test methods and shouldn't be called directly.

        # Because this thing was built in this odd way we are working around it by having the 
        # lambda function set the class vars (g_url, g_username, etc) so that when the runner
        # executes this (with all None parameters) we will apply the class vars.

        # This is a HACK and we need to redo this whole thing.
        
        url = url if url is not None else AddLunarTemplate.g_url
        username = username if username is not None else AddLunarTemplate.g_username
        password = password if password is not None else AddLunarTemplate.g_password
        website_url = website_url if website_url is not None else AddLunarTemplate.g_website_url
        browser_type = browser_type if browser_type is not None else AddLunarTemplate.g_browser_type

        """
        This test is very similar to the 90second website launch, but doesn't navigate to lunar at the end,
        it just ads the site then logs out. This is the test that should be used when stringing together
        a bunch of tests into a suite

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

        # Define webdriver wait and first page
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
        manage_website_page.type_website_url(website_url)
        manage_website_page.click_next()
        utilities.wait_for_page_complete(self.driver)

        manage_website_page.click_lunar_xp()
        utilities.wait_for_page_complete(self.driver)
        manage_website_page.click_next()
        utilities.wait_for_page_complete(self.driver)

        """
        Breaking convention to explain why everything below exists
        Browserstack has a 90 second timeout, where if nothing interacts with the browser for 90 seconds, it times out.
        On larger solodev deployments, it takes longer than 90 seconds for the lunar xl website to deploy. 
        The problem is, selenium waits for the page to "complete" until executing the next command, and
        the Solodev CMS streams logs to the page while deploying a site, so the page doesn't complete. We are stuck.

        To get around that, when we create the browser, we set the page_load_strategy to "none" in the desired 
        capabilities, which mean selenium doesn't wait at all before the next command executes. 
        (this is why every step has a wait after it)
        Chrome and Firefox handle this differently (blame Google, their webdriver isn't up to spec)
        The selenium 'wait.until(expected conditions)' is considered interacting with the browser so,
        Firefox: 
        We set a timeout to cause an exception, handle this exception, then we can interact with the browser. 
        Browserstack considers checking for an elements existence as an interaction with the browser, so we just
        keep checking for the existence of the next link we want to click, and it waits until the 
        1200s wait timer is up.
        Chrome:
        Chrome doesn't timeout properly, and kills the browser, so we can't use the Firefox method (which is 'correct').
        Instead, the page is considered 'interactive' while loading, before it reaches complete, we keep checking that
        status, which browserstack also considers interacting with the browser, then just to be doubly sure, we 
        also check for the existence of the next link we want to click, up to the same 1200s.
        """
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

        websites_dev_page = WebsitesDevPage(self.driver)
        websites_dev_page.expand_folder("www")
        utilities.wait_for_page_complete(self.driver)
        websites_dev_page.click_page("index.stml")
        utilities.wait_for_page_complete(self.driver)

        #there might need to be an extra step here, like clicking the site header/logo to go home
        home_page = HomePage(self.driver)
        utilities.wait_for_page_complete(self.driver)
        home_page.click_profile()
        utilities.wait_for_page_complete(self.driver)
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


