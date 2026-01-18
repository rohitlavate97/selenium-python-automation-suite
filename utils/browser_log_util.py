import allure
from core.driver_factory import DriverFactory
from utils.log_util import LogUtil


class BrowserLogUtil:

    @staticmethod
    def attach_console_logs():
        logger = LogUtil.get_logger("BrowserLogUtil")
        driver = DriverFactory.get_driver()

        try:
            logs = driver.get_log("browser")
            log_text = "\n".join([str(entry) for entry in logs])

            allure.attach(
                log_text,
                name="Browser Console Logs",
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info("Browser logs attached to Allure")
            LogUtil.log_json("Browser logs attached")

        except Exception as e:
            logger.warning(f"Browser logs not supported: {e}")
            LogUtil.log_json(
                "Browser logs not supported",
                level="WARN",
                extra={"error": str(e)}
            )
