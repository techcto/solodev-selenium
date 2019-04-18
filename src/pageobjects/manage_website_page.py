from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class ManageWebsitePage(BasePage):

    def click_update_website(self):
        self.driver.find_element_by_link_text("Update Website").click()

    def click_settings(self):
        self.driver.find_element_by_css_selector("a[data-name='Settings']").click()

    def click_redirects(self):
        self.driver.find_element_by_link_text("Redirects").click()

    def click_permissions(self):
        self.driver.find_element_by_link_text("Permissions").click()

    # Deleting the website is a 2 step process, type then click, so they are 2 steps here too
    def delete_site(self):
        delete_text_field = self.driver.find_element_by_css_selector("#confirm_delete")
        delete_button = self.driver.find_element_by_css_selector(".delete_website.btn.btn-scarlet")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        delete_text_field.send_keys("DELETE")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        delete_button.click()

    # Expand sections in the various panels
    # Settings
    def toggle_domain_information(self):
        element = self.driver.find_element_by_css_selector("#headingDomain")
        element.click()

    def toggle_ssl_information(self):
        element = self.driver.find_element_by_css_selector("#headingSSL")
        element.click()

    def toggle_payment_information(self):
        element = self.driver.find_element_by_css_selector("#headingPayment")
        element.click()

    def toggle_advanced(self):
        element = self.driver.find_element_by_css_selector("#headingAdvanced")
        element.click()

    # The below go through the process of adding a new website
    # Maybe they can have their own page if this gets too big?

    def type_website_url(self, website_url):
        self.driver.find_element_by_css_selector("#name").send_keys(website_url)

    def click_next(self):
        self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Next']")))
        self.driver.find_element_by_css_selector("input[value='Next']").click()

    def click_lunar_xp(self):
        self.driver.find_element_by_css_selector("img[alt='LunarXP Theme']").click()

    def click_blank_website(self):
        self.driver.find_element_by_css_selector("img[alt='Building Theme']").click()
        select = Select(self.driver.find_element_by_id("custom_select"))
        select.select_by_visible_text("Blank Website")

    def custom_upload_theme(self):
        self.driver.find_element_by_css_selector("img[alt='Building Theme']").click()
        select = Select(self.driver.find_element_by_id("custom_select"))
        select.select_by_visible_text("Upload Theme")

    def click_start_managing(self):
        self.driver.find_element_by_link_text("Start Managing Your Website").click()
