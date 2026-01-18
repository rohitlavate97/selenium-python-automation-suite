from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.driver_factory import DriverFactory
from core.framework_constants import EXPLICIT_WAIT

class SeleniumUtil:

    @staticmethod
    def click(element):
        WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.element_to_be_clickable(element)).click()

    @staticmethod
    def type(element, text):
        WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.visibility_of(element))
        element.clear()
        element.send_keys(text)

    @staticmethod
    def get_text(element):
        return WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.visibility_of(element)).text
