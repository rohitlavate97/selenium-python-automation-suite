from selenium.webdriver.common.by import By
from utils.selenium_utils import SeleniumUtil
from pages.base_page import BasePage
from utils.step_logger import log_step


class LoginPage(BasePage):

    username = (By.ID, "username")
    password = (By.NAME, "pwd")
    login_btn = (By.XPATH, "//div[text()='Login ']")

    @log_step("Enter username")
    def enter_username(self, user):
        SeleniumUtil.type(self.driver.find_element(*self.username), user)

    @log_step("Enter password")
    def enter_password(self, pwd):
        SeleniumUtil.type(self.driver.find_element(*self.password), pwd)

    @log_step("Click login")
    def click_login(self):
        SeleniumUtil.click(self.driver.find_element(*self.login_btn))

    @log_step("Perform login")
    def login(self, user, pwd):
        self.enter_username(user)
        self.enter_password(pwd)
        self.click_login()
