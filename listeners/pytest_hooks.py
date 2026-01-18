import pytest
import subprocess
from utils.email_util import EmailUtil
from utils.config_reader import ConfigReader
from utils.slack_util import SlackUtil
from utils.video_util import VideoUtil
from utils.cleanup_util import CleanupUtil


# ---------------------------
# CLEANUP BEFORE TESTS START
# ---------------------------
def pytest_sessionstart(session):
    print("🧹 Cleaning old artifacts before test run...")
    CleanupUtil.clean_all()


# ---------------------------
# AFTER ALL TESTS FINISH
# ---------------------------
def pytest_sessionfinish(session, exitstatus):
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
        print("Allure HTML report generated successfully.")
    except Exception as e:
        print("Failed to generate Allure report:", e)

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

    # ---------------------------
    # Slack Notification
    # ---------------------------
    SlackUtil.send_message(
        webhook_url="YOUR_WEBHOOK_URL",
        message="🚀 Automation Execution Completed. Allure report generated!"
    )
