from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class PageSyncUtil:

    @staticmethod
    def wait_for_dom_ready(driver, timeout=15):
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            # Don't fail test for DOM wait
            pass

    @staticmethod
    def wait_for_network_idle(driver, timeout=10):
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("""
                    return (typeof window.pendingRequests === 'undefined') 
                           || window.pendingRequests === 0;
                """)
            )
        except TimeoutException:
            # Don't fail test for background network
            pass

    @staticmethod
    def wait_for_ui_stable(driver, timeout=15):
        PageSyncUtil.wait_for_dom_ready(driver, timeout)
        PageSyncUtil.wait_for_network_idle(driver, timeout)
