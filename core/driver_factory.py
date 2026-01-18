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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import local

_driver = local()


class DriverFactory:

    @staticmethod
    def init_driver(
            browser="chrome",
            headless=False,
            grid=False,
            grid_url=None
    ):
        browser = browser.lower()

        if grid:
            if browser == "chrome":
                options = Options()
                if headless:
                    options.add_argument("--headless=new")

                options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

            elif browser == "edge":
                options = EdgeOptions()
                if headless:
                    options.add_argument("--headless=new")

                options.set_capability("ms:loggingPrefs", {"browser": "ALL"})

            elif browser == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("-headless")

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

                options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

                service = Service(ChromeDriverManager().install())
                _driver.instance = webdriver.Chrome(
                    service=service,
                    options=options
                )

            elif browser == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("-headless")

                service = FirefoxService(GeckoDriverManager().install())
                _driver.instance = webdriver.Firefox(
                    service=service,
                    options=options
                )

            elif browser == "edge":
                options = EdgeOptions()
                if headless:
                    options.add_argument("--headless=new")

                options.set_capability("ms:loggingPrefs", {"browser": "ALL"})

                service = EdgeService(EdgeChromiumDriverManager().install())
                _driver.instance = webdriver.Edge(
                    service=service,
                    options=options
                )

            else:
                raise Exception(f"Unsupported browser: {browser}")

        _driver.instance.maximize_window()
        return _driver.instance

    @staticmethod
    def get_driver():
        if not hasattr(_driver, "instance"):
            raise Exception("Driver not initialized. Call init_driver() first.")
        return _driver.instance

    @staticmethod
    def quit_driver():
        if hasattr(_driver, "instance"):
            try:
                _driver.instance.quit()
            except Exception:
                pass
            finally:
                del _driver.instance
