import os
import allure
from datetime import datetime
from core.driver_factory import DriverFactory

class PageSourceUtil:

    @staticmethod
    def dump_source(name="page_source"):
        driver = DriverFactory.get_driver()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        os.makedirs("pagesource", exist_ok=True)
        path = f"pagesource/{name}_{timestamp}.html"

        with open(path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        return path

    @staticmethod
    def attach_to_allure():
        driver = DriverFactory.get_driver()
        source = driver.page_source
        allure.attach(
            source,
            name="Page Source",
            attachment_type=allure.attachment_type.HTML
        )
