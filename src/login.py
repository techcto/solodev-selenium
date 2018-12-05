from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Login():
    def __init__(self):
        self.driver = webdriver
    
    def test(self):
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

        driver.get("http://54.157.157.208/")
        if not "Solodev" in driver.title:
            raise Exception("Unable to load Solodev!")

        #Login
        mail = driver.find_element_by_name("mail")
        password = driver.find_element_by_name("solodevpassword")
        mail.send_keys("solodev")
        password.send_keys("password")
        driver.find_element_by_xpath("//button[@type='submit']").click()

        print(driver.title)
        driver.quit()