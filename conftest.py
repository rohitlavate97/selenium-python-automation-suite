import pytest
from core.driver_factory import DriverFactory
from utils.config_reader import ConfigReader

# ----------------------------
# CLI OPTIONS
# ----------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment name (qa / uat / prod)"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser name (chrome / firefox / edge)"
    )

# ----------------------------
# FIXTURES FOR CLI OPTIONS
# ----------------------------
@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

# ----------------------------
# WEBDRIVER SETUP / TEARDOWN
# ----------------------------
@pytest.fixture(scope="function", autouse=True)
def setup(request, browser):
    """
    This fixture:
    1. Runs BEFORE every test
    2. Loads env config
    3. Opens the application
    4. Quits WebDriver AFTER test
    """
    env_name = request.config.getoption("--env")
    config = ConfigReader.load(env_name)

    driver = DriverFactory.init_driver(
        browser=browser,
        headless=config["HEADLESS"],
        grid=config["GRID"],
        grid_url=config["GRID_URL"]
    )

    driver.get(config["URL"])
    yield
    DriverFactory.quit_driver()
