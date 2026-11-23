from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


class HomeScreen:
    HOME_TAB = (AppiumBy.ACCESSIBILITY_ID, "HOME")
    SEARCH_TAB = (AppiumBy.ACCESSIBILITY_ID, "SEARCH")

    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self):
        WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(self.HOME_TAB)
        )
        return True

    def navigate_home(self):
        if not self.driver.find_elements(*self.HOME_TAB):
            self.driver.back()

        WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(self.HOME_TAB)
        )
        self.driver.find_element(*self.HOME_TAB).click()
        return self.wait_until_loaded()

    def open_search(self):
        self.driver.find_element(*self.SEARCH_TAB).click()

        # The Compose search bar has no tappable accessibility node until opened.
        window_size = self.driver.get_window_size()
        self.driver.execute_script(
            "mobile: clickGesture",
            {
                "x": window_size["width"] // 2,
                "y": int(window_size["height"] * 0.05),
            },
        )
