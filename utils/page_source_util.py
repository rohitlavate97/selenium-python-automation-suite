import os
import allure
from datetime import datetime
from core.driver_factory import DriverFactory
from utils.log_util import LogUtil


class PageSourceUtil:

    @staticmethod
    def dump_source(name="page_source"):
        logger = LogUtil.get_logger("PageSourceUtil")
        driver = DriverFactory.get_driver()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        os.makedirs("pagesource", exist_ok=True)
        path = f"pagesource/{name}_{timestamp}.html"

        with open(path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        logger.info(f"Page source dumped: {path}")
        LogUtil.log_json("Page source dumped", extra={"path": path})

        return path

    @staticmethod
    def attach_to_allure():
        logger = LogUtil.get_logger("PageSourceUtil")
        driver = DriverFactory.get_driver()
        source = driver.page_source

        allure.attach(
            source,
            name="Page Source",
            attachment_type=allure.attachment_type.HTML
        )

        logger.info("Page source attached to Allure")
        LogUtil.log_json("Page source attached to Allure")
