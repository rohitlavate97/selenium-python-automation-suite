import pytest
from core.driver_factory import DriverFactory
from utils.config_reader import ConfigReader

@pytest.fixture(scope="function", autouse=True)
def setup(request):
    env = request.config.getoption("--env")
    browser = request.config.getoption("--browser")

    config = ConfigReader.load(env)

    driver = DriverFactory.init_driver(
        browser=browser,
        headless=config["HEADLESS"],
        grid=config["GRID"],
        grid_url=config["GRID_URL"]
    )

    driver.get(config["URL"])
    yield
    DriverFactory.quit_driver()
