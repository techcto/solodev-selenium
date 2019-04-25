import time
from selenium.webdriver.support.wait import WebDriverWait


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
        """
        For the left nav when developing a website, expanding a folder
        :param name: string, name of the folder to expand
        :return:
        """
        nodes = self.driver.find_elements_by_class_name("tree-node")

        for i, n in enumerate(nodes, start=1):
            if name in self.driver.find_element_by_id("_easyui_tree_{}".format(i)).text:
                self.driver.find_element_by_css_selector("#_easyui_tree_{}".format(i)+" > .tree-hit").click()
                time.sleep(1)

    def click_page(self, name):
        """
        For the left nav when developing a website, clicking a specific page/file
        :param name: string, page/file name, including extension if present
        :return:
        """
        nodes = self.driver.find_elements_by_class_name("tree-node")

        for i, n in enumerate(nodes, start=1):
            if name in self.driver.find_element_by_id("_easyui_tree_{}".format(i)).text:
                self.driver.find_element_by_css_selector("#_easyui_tree_{}".format(i)+" > .tree-title").click()
                time.sleep(1)

    def click_folder(self, name):
        """
        For the left nav when developing a website, clicking a specific folder by name
        :param name: string, name of the folder
        :return:
        """
        nodes = self.driver.find_elements_by_id("tree-node")

        for i, n in enumerate(nodes, start=1):
            if name in self.driver.find_element_by_id("_easyui_tree_{}".format(i)).text:
                self.driver.find_element_by_css_selector("#_easyui_tree_{}".format(i)+" > .tree-title").click()
                time.sleep(1)

