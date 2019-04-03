from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class WebsitesDevPage(BasePage):
    def find_site_name(self, name):
        return True
        # TODO locator for site name
        # return self.driver.find_element_by_xpath("//*[@id'dashboard-nav']/div/div/a/span").getText()

    def expand_folder(self, name):
        nodes = self.driver.find_elements_by_id("tree-node")
        i = 1

        for n in nodes:
            if self.driver.find_element_by_id("_easyui_tree_"+i+"").text in name:
                self.driver.find_element_by_css_selector("_easyui_tree_"+i+" > span.tree-title").click()
            i = i + 1

    def click_page(self, name):
        nodes = self.driver.find_elements_by_id("tree-node")
        i = 1

        for n in nodes:
            if self.driver.find_element_by_id("_easyui_tree_"+i+"").text in name:
                self.driver.find_element_by_css_selector("_easyui_tree_"+i+" > span.tree-title").click()
            i = i + 1

