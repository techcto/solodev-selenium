from selenium.webdriver.support.wait import WebDriverWait

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

class HomePage(BasePage):

    # CLICK THINGS
    # logo at the top of the page
    def click_logo(self):
        self.driver.find_element_by_css_selector(".logo").click()

    # click nav buttons
    # Workspace
    def click_websites(self):
        self.driver.find_element_by_id("websites").click()

    def click_managers(self):
        self.driver.find_element_by_id("Managers").click()

    def click_documentation(self):
        self.driver.find_element_by_id("Documents").click()

    # Organization
    def click_users(self):
        self.driver.find_element_by_id("users").click()

    def click_groups(self):
        self.driver.find_element_by_id("groups").click()

    # Settings
    def click_permissions(self):
        self.driver.find_element_by_id("permissions").click()

    def click_apps(self):
        self.driver.find_element_by_id("apps").click()

    def click_workflow(self):
        self.driver.find_element_by_id("workflow").click()

    def click_reports(self):
        self.driver.find_element_by_id("reports").click()

    def click_advanced(self):
        self.driver.find_element_by_id("advanced").click()

    def click_branding(self):
        self.driver.find_element_by_id("branding").click()

    # Support
    def click_docs(self):
        self.driver.find_element_by_id("docs").click()

    def click_roadmap(self):
        self.driver.find_element_by_id("roadmap").click()

    def click_contact(self):
        self.driver.find_element_by_id("contact").click()

    # profile
    def click_profile(self):
        self.driver.find_element_by_css_selector(".user-avatar").click()

    def click_logout(self):
        self.driver.find_element_by_css_selector('[aria-label="Log Out"]').click()
        self.driver.implicitly_wait(2)

    def click_gotoprofile(self):
        self.driver.find_element_by_css_selector('[aria-label="Go to Profile"]').click()

    # Rest Of The Page - click something in the grid
    # Websites
    def click_a_website(self):
        self.driver.find_element_by_css_selector().click()

    # Managers
    def click_a_manager(self):
        self.driver.find_element_by_css_selector().click()
