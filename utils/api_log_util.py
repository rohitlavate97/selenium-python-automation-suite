import allure
from utils.log_util import LogUtil


class ApiLogUtil:

    @staticmethod
    def log_request(method, url, headers=None, body=None):
        logger = LogUtil.get_logger("API")
        logger.info(f"API REQUEST: {method} {url}")
        LogUtil.log_json("API request", extra={
            "method": method,
            "url": url
        })

        allure.attach(
            f"{method} {url}\nHeaders: {headers}\nBody: {body}",
            name="API Request",
            attachment_type=allure.attachment_type.TEXT
        )

    @staticmethod
    def log_response(status, body):
        logger = LogUtil.get_logger("API")
        logger.info(f"API RESPONSE: {status}")
        LogUtil.log_json("API response", extra={
            "status": status
        })

        allure.attach(
            str(body),
            name="API Response",
            attachment_type=allure.attachment_type.JSON
        )
