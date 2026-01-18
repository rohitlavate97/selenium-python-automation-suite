import os
import allure
from datetime import datetime
from core.driver_factory import DriverFactory
from utils.log_util import LogUtil


class ScreenshotUtil:

    @staticmethod
    def capture(name="screenshot"):
        logger = LogUtil.get_logger("ScreenshotUtil")
        driver = DriverFactory.get_driver()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        os.makedirs("screenshots", exist_ok=True)

        path = f"screenshots/{name}_{timestamp}.png"
        driver.save_screenshot(path)

        logger.info(f"Screenshot captured: {path}")
        LogUtil.log_json("Screenshot captured", extra={"path": path})

        return path

    @staticmethod
    def attach_to_allure():
        logger = LogUtil.get_logger("ScreenshotUtil")
        driver = DriverFactory.get_driver()
        png = driver.get_screenshot_as_png()

        allure.attach(
            png,
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        logger.info("Screenshot attached to Allure")
        LogUtil.log_json("Screenshot attached to Allure")
