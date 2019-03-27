import unittest
from src.values import strings
from src.pageobjects.login_page import LoginPage
from src.pageobjects.home_page import HomePage
from selenium import webdriver


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(strings.localhost_solodev_url)
        self.driver.maximize_window()

    def test_login(self):
        # Define webdriver wait and first page
        login_page = LoginPage(self.driver)
        home_page = HomePage(self.driver)

        if "Solodev" not in self.driver.title:
            raise Exception("Unable to load Solodev!")

        # Login
        login_page.type_login(strings.username, strings.password)
        login_page.click_login()

        # Log out
        home_page.click_profile()
        home_page.click_logout()

        # Assert we're back on login page
        self.assertTrue(login_page.login_button_present())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

