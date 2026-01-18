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
from utils.page_sync_util import PageSyncUtil

from utils.retry_engine import RetryEngine
from utils.flaky_tracker import FlakyTracker
from utils.stability_analyzer import StabilityAnalyzer
from utils.failure_classifier import FailureClassifier
from utils.analytics_engine import AnalyticsEngine


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
    PageSyncUtil.wait_for_ui_stable(driver)

    yield

    DriverFactory.quit_driver()


# ----------------------------
# SMART RETRY ENGINE
# ----------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    test_name = item.name

    while True:
        try:
            RetryEngine.record_attempt(test_name)
            yield
            return
        except Exception as e:
            if RetryEngine.should_retry(test_name):
                RetryEngine.attach_retry_info(test_name, e)
                AnalyticsEngine.record(test_name, "retries", RetryEngine.attempts[test_name])
                continue
            else:
                raise


# ----------------------------
# FAILURE + FLAKY + ANALYTICS
# ----------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        status = "failed" if rep.failed else "passed"
        FlakyTracker.record(item.name, status)

        history = FlakyTracker.load().get(item.name, [])
        stability = StabilityAnalyzer.stability_score(history)

        AnalyticsEngine.record(item.name, "stability", stability)
        allure.dynamic.label("stability", f"{stability}%")

        if FlakyTracker.is_flaky(history):
            allure.dynamic.label("flaky", "true")
            allure.attach(
                f"Stability Score: {stability}%",
                name="Flakiness Analysis",
                attachment_type=allure.attachment_type.TEXT
            )

    if rep.when == "call" and rep.failed:
        exc = call.excinfo.value if call.excinfo else None
        if exc:
            category = FailureClassifier.classify(exc)
            allure.dynamic.label("failure_type", category)
            AnalyticsEngine.record(item.name, "failure_type", category)

        try:
            ScreenshotUtil.attach_to_allure()
            PageSourceUtil.attach_to_allure()
            BrowserLogUtil.attach_console_logs()

            if os.path.exists("logs/structured.json"):
                with open("logs/structured.json", "r", encoding="utf-8") as f:
                    allure.attach(
                        f.read(),
                        name="Structured Logs",
                        attachment_type=allure.attachment_type.JSON
                    )

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

    env = session.config.getoption("--env")
    config = ConfigReader.load(env)

    # ---------------------------
    # Generate Allure Report (Windows-safe)
    # ---------------------------
    try:
        subprocess.run(
            "allure generate allure-results -o allure-report --clean",
            check=True,
            shell=True
        )
        print("✅ Allure report generated")
    except Exception as e:
        print("❌ Allure generation failed:", e)

    # ---------------------------
    # Email Notification (Optional)
    # ---------------------------
    try:
        if "EMAIL" in config and config["EMAIL"].get("FROM") and config["EMAIL"].get("PASSWORD"):
            EmailUtil.send_email(
                subject="Automation Execution Completed",
                body="<h2>Execution Finished</h2>",
                sender=config["EMAIL"]["FROM"],
                password=config["EMAIL"]["PASSWORD"],
                recipients=config["EMAIL"]["TO"],
                attachments=["allure-report/index.html"]
            )
            print("📧 Email sent")
        else:
            print("ℹ️ Email skipped (not configured)")
    except Exception as e:
        print("❌ Email failed:", e)

    # ---------------------------
    # Slack Notification (Optional)
    # ---------------------------
    try:
        webhook = "YOUR_WEBHOOK_URL"
        if webhook.startswith("http"):
            SlackUtil.send_message(
                webhook_url=webhook,
                message="🚀 Automation completed. Allure report ready."
            )
            print("💬 Slack notified")
        else:
            print("ℹ️ Slack skipped (not configured)")
    except Exception as e:
        print("❌ Slack failed:", e)
