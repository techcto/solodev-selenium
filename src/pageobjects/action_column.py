from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


# taking actions like move, copy, add various items, and delete items
# must switch to the iframe in the actual test, before calling one of these
class ActionColumn(BasePage):

    def click_permissions(self):
        self.driver.find_element_by_css_selector("data-name=\"Permissions\"").click()

    def click_update_folder(self):
        self.driver.find_element_by_css_selector("data-name=\"Update Folder\"").click()

    def click_publish(self):
        self.driver.find_element_by_css_selector("data-name=\"Publish\"").click()

    def click_stage(self):
        self.driver.find_element_by_css_selector("data-name=\"Stage\"").click()

    def click_delete(self):
        self.driver.find_element_by_css_selector("data-name=\"Delete\"").click()

    def click_move(self):
        self.driver.find_element_by_css_selector("data-name=\"Move\"").click()

    def click_copy(self):
        self.driver.find_element_by_css_selector("data-name=\"Copy\"").click()

    def click_add_scheduler(self):
        self.driver.find_element_by_css_selector("data-name=\"Add Scheduler\"").click()

    def click_add_experiment(self):
        self.driver.find_element_by_css_selector("data-name=\"Add Experiment\"").click()

    def click_add_group(self):
        self.driver.find_element_by_css_selector("data-name=\"Add Group\"").click()

    def click_add_link(self):
        self.driver.find_element_by_css_selector("data-name=\"Add Link\"").click()

    def click_add_page(self):
        self.driver.find_element_by_css_selector("data-name=\"Add Page\"").click()

    def click_add_file(self):
        self.driver.find_element_by_css_selector("data-name=\"Add File\"").click()

    def click_add_folder(self):
        self.driver.find_element_by_css_selector("data-name=\"Add Folder\"").click()

    def click_upload(self):
        self.driver.find_element_by_css_selector("data-name=\"Upload\"").click()

