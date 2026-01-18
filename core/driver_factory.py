from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from threading import local

from utils.log_util import LogUtil
from utils.network_tracker import NetworkTracker

_driver = local()


class DriverFactory:

    @staticmethod
    def init_driver(browser="chrome", headless=False, grid=False, grid_url=None):
        logger = LogUtil.get_logger("DriverFactory")

        LogUtil.log_json("Initializing driver", extra={
            "browser": browser,
            "headless": headless,
            "grid": grid
        })

        browser = browser.lower()

        try:
            if grid:
                if browser == "chrome":
                    options = Options()
                    if headless:
                        options.add_argument("--headless=new")
                elif browser == "firefox":
                    options = FirefoxOptions()
                    if headless:
                        options.add_argument("-headless")
                elif browser == "edge":
                    options = EdgeOptions()
                    if headless:
                        options.add_argument("--headless=new")
                else:
                    raise Exception(f"Unsupported browser: {browser}")

                _driver.instance = webdriver.Remote(
                    command_executor=grid_url,
                    options=options
                )
            else:
                if browser == "chrome":
                    options = Options()
                    if headless:
                        options.add_argument("--headless=new")
                    service = Service(ChromeDriverManager().install())
                    _driver.instance = webdriver.Chrome(service=service, options=options)

                elif browser == "firefox":
                    options = FirefoxOptions()
                    if headless:
                        options.add_argument("-headless")
                    service = FirefoxService(GeckoDriverManager().install())
                    _driver.instance = webdriver.Firefox(service=service, options=options)

                elif browser == "edge":
                    options = EdgeOptions()
                    if headless:
                        options.add_argument("--headless=new")
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    _driver.instance = webdriver.Edge(service=service, options=options)

                else:
                    raise Exception(f"Unsupported browser: {browser}")

            _driver.instance.maximize_window()

            # ✅ Inject network tracker safely
            try:
                NetworkTracker.inject(_driver.instance)
                logger.info("Network tracker injected successfully")
            except Exception as e:
                logger.warning(f"Network tracker injection failed: {e}")

            logger.info("Driver initialized successfully")
            return _driver.instance

        except Exception as e:
            logger.error(f"Driver init failed: {e}")
            raise

    @staticmethod
    def get_driver():
        if not hasattr(_driver, "instance"):
            raise Exception("Driver not initialized.")
        return _driver.instance

    @staticmethod
    def quit_driver():
        logger = LogUtil.get_logger("DriverFactory")

        if hasattr(_driver, "instance"):
            try:
                _driver.instance.quit()
                logger.info("Driver quit successfully")
            except Exception as e:
                logger.error(f"Driver quit failed: {e}")
            finally:
                del _driver.instance
