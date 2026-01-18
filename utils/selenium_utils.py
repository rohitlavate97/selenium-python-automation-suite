from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.driver_factory import DriverFactory
from core.framework_constants import EXPLICIT_WAIT
from utils.log_util import LogUtil


class SeleniumUtil:

    @staticmethod
    def click(element):
        logger = LogUtil.get_logger("SeleniumUtil")
        logger.info("Clicking element")
        LogUtil.log_json("Clicking element", extra={"action": "click"})

        WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.element_to_be_clickable(element))
        element.click()

    @staticmethod
    def type(element, text):
        logger = LogUtil.get_logger("SeleniumUtil")
        masked = "*" * len(str(text))

        logger.info("Typing into element")
        LogUtil.log_json("Typing into element", extra={
            "action": "type",
            "value": masked
        })

        WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.visibility_of(element))
        element.clear()
        element.send_keys(text)

    @staticmethod
    def get_text(element):
        logger = LogUtil.get_logger("SeleniumUtil")
        logger.info("Fetching element text")
        LogUtil.log_json("Fetching element text", extra={"action": "get_text"})

        return WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.visibility_of(element)).text
