from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


class HomeScreen:
    HOME_TAB = (AppiumBy.ACCESSIBILITY_ID, "HOME")

    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self):
        WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(self.HOME_TAB)
        )
        return True
