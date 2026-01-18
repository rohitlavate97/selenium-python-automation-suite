from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.driver_factory import DriverFactory
from core.framework_constants import EXPLICIT_WAIT
from utils.log_util import LogUtil


class WaitUtil:

    @staticmethod
    def wait_for_visible(locator):
        logger = LogUtil.get_logger("WaitUtil")
        logger.info(f"Waiting for visibility: {locator}")
        LogUtil.log_json("Waiting for visibility", extra={"locator": str(locator)})

        return WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.visibility_of_element_located(locator))

    @staticmethod
    def wait_for_clickable(locator):
        logger = LogUtil.get_logger("WaitUtil")
        logger.info(f"Waiting for clickable: {locator}")
        LogUtil.log_json("Waiting for clickable", extra={"locator": str(locator)})

        return WebDriverWait(DriverFactory.get_driver(), EXPLICIT_WAIT)\
            .until(EC.element_to_be_clickable(locator))
