from core.driver_factory import DriverFactory

class BasePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
