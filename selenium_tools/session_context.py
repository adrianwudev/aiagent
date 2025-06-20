from selenium import webdriver

class SeleniumSessionContext:
    """
    Manage a shared Selenium WebDriver session for agent tools.
    Use get_driver() to get the current driver, and close() to quit the session.
    This class is a true singleton: all imports and usages share the same driver instance.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.driver = None
        return cls._instance

    def get_driver(self):
        if self.driver is None:
            print("[SeleniumSessionContext] Creating new WebDriver instance.")
            self.driver = webdriver.Chrome()
        return self.driver

    def close(self):
        if self.driver is not None:
            print("[SeleniumSessionContext] Closing WebDriver instance.")
            self.driver.quit()
            self.driver = None 