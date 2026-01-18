from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.driver_factory import DriverFactory
from core.framework_constants import EXPLICIT_WAIT
from utils.log_util import LogUtil
from utils.page_sync_util import PageSyncUtil


class SeleniumUtil:

    @staticmethod
    def click(element):
        logger = LogUtil.get_logger("SeleniumUtil")
        logger.info("Clicking element")

        driver = DriverFactory.get_driver()

        WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(element)
        )

        element.click()
        PageSyncUtil.wait_for_ui_stable(driver)

    @staticmethod
    def type(element, text):
        logger = LogUtil.get_logger("SeleniumUtil")
        logger.info("Typing into element")

        driver = DriverFactory.get_driver()

        WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.visibility_of(element)
        )

        element.clear()
        element.send_keys(text)

        PageSyncUtil.wait_for_ui_stable(driver)

    @staticmethod
    def get_text(element):
        driver = DriverFactory.get_driver()

        text = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.visibility_of(element)
        ).text

        PageSyncUtil.wait_for_ui_stable(driver)
        return text
