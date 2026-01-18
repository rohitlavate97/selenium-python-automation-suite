import os
import allure
from datetime import datetime
from selenium.webdriver.common.by import By
from core.driver_factory import DriverFactory

class ScreenshotUtil:

    @staticmethod
    def capture(name="screenshot"):
        driver = DriverFactory.get_driver()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"

        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(path)
        return path

    @staticmethod
    def attach_to_allure():
        driver = DriverFactory.get_driver()
        png = driver.get_screenshot_as_png()
        allure.attach(png, name="Failure Screenshot",
                      attachment_type=allure.attachment_type.PNG)
