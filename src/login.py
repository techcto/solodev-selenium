import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Login():
    def __init__(self):
        self.driver = webdriver
    
    def test(self, url, username, password):
        desired_cap = {
        'browser': 'Chrome',
        'browser_version': '70.0',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '2048x1536'
        }

        driver = webdriver.Remote(
            command_executor= os.getenv("COMMAND_EXECUTOR"),
            desired_capabilities=desired_cap)

        driver.get(url)
        if not "Solodev" in driver.title:
            raise Exception("Unable to load Solodev!")

        #Login
        mail = driver.find_element_by_name("email")
        password = driver.find_element_by_name("password")
        mail.send_keys(username)
        password.send_keys(password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Welcome to Solodev!'])[1]/following::div[1]").click()
        driver.find_element_by_id("name").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("www.testwebsite.com")
        driver.find_element_by_xpath("//div[@id='w4-address']/div").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Next'])[2]/i[1]").click()
        driver.find_element_by_id("w4-address2").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Previous'])[1]/following::a[2]").click()
        driver.find_element_by_id("w4-email").click()
        driver.find_element_by_id("w4-email").clear()
        driver.find_element_by_id("w4-email").send_keys("testemail@email.com")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Welcome to Solodev!'])[1]/following::div[1]").click()
        driver.find_element_by_id("w4-terms").click()
        driver.find_element_by_link_text("Finish").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Websites'])[1]/following::span[4]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Location:'])[1]/following::div[2]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Update Website'])[1]/following::span[3]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Accept Discover'])[1]/following::h2[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Import / Export'])[1]/following::span[3]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Next'])[1]/preceding::div[5]").click()
        driver.find_element_by_id("uploadFile").click()
        driver.find_element_by_id("uploadFile").clear()
        driver.find_element_by_id("uploadFile").send_keys("C:\\Users\\admin\\Desktop\\01_Package_Tests\\package_scss.zip")
        driver.find_element_by_link_text("Next").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='+'])[1]/following::a[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Previous'])[1]/following::a[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='robots.txt'])[1]").click()

        print(driver.title)
        driver.quit()