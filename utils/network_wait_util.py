from selenium.webdriver.support.ui import WebDriverWait
from core.driver_factory import DriverFactory

class NetworkWaitUtil:

    @staticmethod
    def wait_for_network_idle(timeout=15):
        driver = DriverFactory.get_driver()

        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("""
                return (window.pendingRequests || 0) === 0;
            """)
        )
