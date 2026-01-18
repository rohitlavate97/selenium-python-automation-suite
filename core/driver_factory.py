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

_driver = local()

class DriverFactory:

    @staticmethod
    def init_driver(
            browser="chrome",
            headless=False,
            grid=False,
            grid_url=None
    ):
        if grid:
            options = Options()
            if headless:
                options.add_argument("--headless")
            _driver.instance = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )
        else:
            if browser == "chrome":
                options = Options()
                if headless:
                    options.add_argument("--headless")
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
                    options.add_argument("--headless")
                service = EdgeService(EdgeChromiumDriverManager().install())
                _driver.instance = webdriver.Edge(
                    service=service,
                    options=options
                )

        _driver.instance.maximize_window()
        return _driver.instance

    @staticmethod
    def get_driver():
        return _driver.instance

    @staticmethod
    def quit_driver():
        if hasattr(_driver, "instance"):
            _driver.instance.quit()
            del _driver.instance
