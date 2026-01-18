import pytest
import subprocess
import os
import json
import allure

from core.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
from utils.cleanup_util import CleanupUtil
from utils.email_util import EmailUtil
from utils.slack_util import SlackUtil
from utils.screenshot_util import ScreenshotUtil
from utils.page_source_util import PageSourceUtil
from utils.browser_log_util import BrowserLogUtil
from utils.log_util import LogUtil


# ----------------------------
# CLI OPTIONS
# ----------------------------
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa")
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


# ----------------------------
# CLEANUP BEFORE SESSION
# ----------------------------
def pytest_sessionstart(session):
    print("🧹 Cleaning old artifacts...")
    CleanupUtil.clean_all()


# ----------------------------
# TEST CONTEXT + LOGGER
# ----------------------------
@pytest.fixture(autouse=True)
def test_context(request, env, browser):
    test_name = request.node.name
    cid = LogUtil.set_context(test_name, env, browser)

    logger = LogUtil.get_logger(test_name)
    logger.info(f"🚀 Test started | CID={cid}")
    LogUtil.log_json("Test started")

    yield

    logger.info(f"🏁 Test finished | CID={cid}")
    LogUtil.log_json("Test finished")


# ----------------------------
# DRIVER SETUP / TEARDOWN
# ----------------------------
@pytest.fixture(scope="function", autouse=True)
def setup(request, browser):
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
# FAILURE HOOK
# ----------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Attach UI artifacts
            ScreenshotUtil.attach_to_allure()
            PageSourceUtil.attach_to_allure()
            BrowserLogUtil.attach_console_logs()

            # Attach structured logs
            if os.path.exists("logs/structured.json"):
                with open("logs/structured.json", "r", encoding="utf-8") as f:
                    allure.attach(
                        f.read(),
                        name="Structured Logs",
                        attachment_type=allure.attachment_type.JSON
                    )

            # Attach test context
            context = LogUtil.get_context()
            allure.attach(
                json.dumps(context, indent=2),
                name="Test Context",
                attachment_type=allure.attachment_type.JSON
            )

            print("📎 Failure artifacts attached")

        except Exception as e:
            print("❌ Failure hook error:", e)


# ----------------------------
# SESSION FINISH
# ----------------------------
def pytest_sessionfinish(session, exitstatus):
    print("📢 Pytest session finished")

    config = ConfigReader.load("qa")

    # ---------------------------
    # Generate Allure Report
    # ---------------------------
    try:
        subprocess.run(
            ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
            check=True,
            shell=True
        )
        print("✅ Allure report generated")
    except Exception as e:
        print("❌ Allure generation failed:", e)

    # ---------------------------
    # Email Notification
    # ---------------------------
    try:
        EmailUtil.send_email(
            subject="Automation Execution Completed",
            body="<h2>Execution Finished</h2>",
            sender=config["EMAIL"]["FROM"],
            password=config["EMAIL"]["PASSWORD"],
            recipients=config["EMAIL"]["TO"],
            attachments=["allure-report/index.html"]
        )
        print("📧 Email sent")
    except Exception as e:
        print("❌ Email failed:", e)

    # ---------------------------
    # Slack Notification
    # ---------------------------
    try:
        SlackUtil.send_message(
            webhook_url="YOUR_WEBHOOK_URL",
            message="🚀 Automation completed. Allure report ready."
        )
        print("💬 Slack notified")
    except Exception as e:
        print("❌ Slack failed:", e)
