import pytest
import subprocess
from core.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
from utils.cleanup_util import CleanupUtil
from utils.email_util import EmailUtil
from utils.slack_util import SlackUtil

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
# CLEANUP BEFORE TESTS START
# ----------------------------
def pytest_sessionstart(session):
    print("📢 Pytest session started")
    print("🧹 Cleaning old artifacts before test run...")
    CleanupUtil.clean_all()

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

# ----------------------------
# AFTER ALL TESTS FINISH
# ----------------------------
def pytest_sessionfinish(session, exitstatus):
    print("📢 Pytest session finished")

    # Load config
    config = ConfigReader.load("qa")

    # ---------------------------
    # Generate Allure HTML Report
    # ---------------------------
    try:
        subprocess.run(
            ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
            check=True,
            shell=True
        )
        print("✅ Allure HTML report generated successfully.")
    except Exception as e:
        print("❌ Failed to generate Allure report:", e)

    # ---------------------------
    # Email Notification
    # ---------------------------
    subject = "Automation Execution Completed"
    body = "<h2>Test Execution Finished</h2>"

    EmailUtil.send_email(
        subject=subject,
        body=body,
        sender=config["EMAIL"]["FROM"],
        password=config["EMAIL"]["PASSWORD"],
        recipients=config["EMAIL"]["TO"],
        attachments=["allure-report/index.html"]
    )

    print("📧 Email sent successfully")

    # ---------------------------
    # Slack Notification
    # ---------------------------
    SlackUtil.send_message(
        webhook_url="YOUR_WEBHOOK_URL",
        message="🚀 Automation Execution Completed. Allure report generated!"
    )

    print("💬 Slack message sent")
