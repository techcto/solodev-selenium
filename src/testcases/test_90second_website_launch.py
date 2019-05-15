import unittest
import time
import json

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
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


class AddLunarTemplate(unittest.TestCase):

    def setUp(self):
        """
        This is where the driver setup _should_ go, but lambda/browserstack doesn't like it
        I don't think Lambda is aware of unit tests or test suites in general
        Which will break pretty test result reporting in browserstack
        """
        pass
        # self.driver = webdriver.Chrome()

    def test_90second_website_launch(self, url, username, password, website_url, browser_type):

        """
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
        # websites_dev_page.find_site_name()

        websites_dev_page.expand_folder("www")
        utilities.wait_for_page_complete(self.driver)
        websites_dev_page.click_page("index.stml")
        utilities.wait_for_page_complete(self.driver)

        # Open new tab
        # self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
        self.driver.get("http://lunarxp.com")
        utilities.wait_for_page_complete(self.driver)

        hold_key(self.driver, 4)

        # Assert we're at the bottom of the page
        self.assertTrue(len(self.driver.find_elements_by_css_selector(".btn.btn-lg.btn-yellow")) > 0)
        self.driver.quit()

    def tearDown(self):
        """
        This is where driver.quit _should_ go, but because we didn't setup this way, we can't teardown this way
        I don't think Lambda is aware of unit tests or test suites in general
        Which will break pretty test result reporting in browserstack
        """
        pass
        # self.driver.quit()


def dispatch_key_event(driver, name, options={}):
    options["type"] = name
    body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
    resource = "/session/%s/chromium/send_command" % driver.session_id
    locator = driver.command_executor._url + resource
    driver.command_executor._request('POST', locator, body)


def hold_key(driver, duration):
    """
    Function to simulate scrolling down a page. We need to hold the key down inetad of use a scroll bar/wheel
    :param driver: the webdriver
    :param duration: how long to hold down the down key (yes, this only holds the down arrow)
    """
    endtime = time.time() + duration
    options = {
        "type": "<TYPE>",
        "key": "ArrowDown",
        "code": "ArrowDown",
        "nativeVirtualKeyCode": 40,
        "windowsVirtualKeyCode": 40
    }

    while True:
        dispatch_key_event(driver, "rawKeyDown", options)
        dispatch_key_event(driver, "char", options)

        if time.time() > endtime:
            dispatch_key_event(driver, "keyUp", options)
            break

        options["autoRepeat"] = True
        time.sleep(0.01)


def click_element(driver, el):
    """
    Helper function for simulating button clicks while the browser is busy.
    The way we run in Browserstack, this isn't needed, but there might be situations where this is useful.
    Maybe move to utilities?
    """
    def func():
        actions = ActionChains(driver)
        actions.click(el)
        actions.perform()
    return func


# Required for unittest
if __name__ == "__main__":
    unittest.main()

