import time
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class PageEditor(BasePage):

    def click_delete(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-trash']")
        delete.click()

    def click_move(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-paste']")
        delete.click()

    def click_copy(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-copy']")
        delete.click()

    def click_history(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-history']")
        delete.click()

    def click_add_to_group(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-plus-square']")
        delete.click()

    def click_meta(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-info-circle']")
        delete.click()

    def click_publish(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-share-square']")
        delete.click()

    def click_stage(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-cloud-upload-alt']")
        delete.click()

    def click_draft(self):
        delete = self.driver.find_element_by_css_selector("[iconcls='fas fa-save']")
        delete.click()

    def click_submit_action_modal(self):
        self.driver.find_element_by_css_selector(
            "#actionModalForm > div > .modal-content > div > .btn.btn-color1.btn-lg.modal-confirm").click()

    def click_cancel_action_modal(self):
        self.driver.find_element_by_css_selector(
            "#actionModalForm > div > .modal-content > div > .modal-dismiss.backButton").click()

