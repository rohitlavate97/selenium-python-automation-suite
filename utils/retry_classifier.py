from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException
)

class RetryClassifier:

    RETRYABLE = (
        TimeoutException,
        StaleElementReferenceException,
        WebDriverException
    )

    @staticmethod
    def is_retryable(exception):
        return isinstance(exception, RetryClassifier.RETRYABLE)
