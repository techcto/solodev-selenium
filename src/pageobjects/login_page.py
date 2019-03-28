from selenium.webdriver.support.wait import WebDriverWait

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

class LoginPage(BasePage):

    def type_login(self, username, password):
        self.driver.find_element_by_name("email").send_keys(username)
        self.driver.find_element_by_name("password").send_keys(password)

    def click_login(self):
        self.driver.find_element_by_css_selector(".btn.btn-color2.text-white.btn-lg.text-uppercase").click()
        self.driver.implicitly_wait(2)

    def login_button_present(self):
        login_button = self.driver.find_element_by_css_selector(".btn.btn-color2.text-white.btn-lg.text-uppercase")
        return login_button.is_displayed()
