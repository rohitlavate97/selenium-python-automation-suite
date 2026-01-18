from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException
)

class FailureClassifier:

    @staticmethod
    def classify(exception):
        if isinstance(exception, TimeoutException):
            return "Timeout"
        if isinstance(exception, NoSuchElementException):
            return "LocatorIssue"
        if isinstance(exception, StaleElementReferenceException):
            return "DOMMutation"
        if isinstance(exception, WebDriverException):
            return "WebDriver"
        return "Functional"
