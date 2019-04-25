from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class WebsitePage(BasePage):

    def click_add_website(self):
        self.driver.find_element_by_link_text("Add Website").click()

    def find_site_name(self, name):
        return self.driver.find_element_by_xpath("//td[contains(text(), '" + name + "')]")

    def click_site_name(self, name):
        self.find_site_name(name).click()
