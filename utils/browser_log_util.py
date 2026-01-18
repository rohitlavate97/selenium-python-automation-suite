import allure
from core.driver_factory import DriverFactory

class BrowserLogUtil:

    @staticmethod
    def attach_console_logs():
        driver = DriverFactory.get_driver()
        try:
            logs = driver.get_log("browser")
            log_text = "\n".join([str(entry) for entry in logs])

            allure.attach(
                log_text,
                name="Browser Console Logs",
                attachment_type=allure.attachment_type.TEXT
            )
        except Exception as e:
            print("⚠️ Browser logs not supported:", e)
