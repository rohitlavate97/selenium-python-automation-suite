from selenium.webdriver.common.by import By
from utils.selenium_utils import SeleniumUtil
from pages.base_page import BasePage

class LoginPage(BasePage):

    username = (By.XPATH, "//input[@id='username']")
    password = (By.XPATH, "//input[@name='pwd']")
    login_btn = (By.XPATH, "//div[text()='Login ']")

    def login(self, user, pwd):
        SeleniumUtil.type(self.driver.find_element(*self.username), user)
        SeleniumUtil.type(self.driver.find_element(*self.password), pwd)
        SeleniumUtil.click(self.driver.find_element(*self.login_btn))
