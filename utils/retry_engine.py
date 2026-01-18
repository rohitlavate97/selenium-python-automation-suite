import allure
from collections import defaultdict

class RetryEngine:
    MAX_RETRIES = 2
    attempts = defaultdict(int)

    @staticmethod
    def record_attempt(test_name):
        RetryEngine.attempts[test_name] += 1
        return RetryEngine.attempts[test_name]

    @staticmethod
    def should_retry(test_name):
        return RetryEngine.attempts[test_name] <= RetryEngine.MAX_RETRIES

    @staticmethod
    def attach_retry_info(test_name, exception):
        allure.attach(
            str(exception),
            name=f"Retry attempt {RetryEngine.attempts[test_name]}",
            attachment_type=allure.attachment_type.TEXT
        )
