from core.driver_factory import DriverFactory
from utils.log_util import LogUtil


class BasePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.logger = LogUtil.get_logger(self.__class__.__name__)
        self.logger.info(f"{self.__class__.__name__} initialized")
        LogUtil.log_json("Page initialized", extra={
            "page": self.__class__.__name__
        })
