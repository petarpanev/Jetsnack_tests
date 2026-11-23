from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


class SearchScreen:
    SEARCH_FIELD = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    def __init__(self, driver):
        self.driver = driver

    def search_for(self, query: str):
        search_field = WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.SEARCH_FIELD)
        )
        search_field.send_keys(query)

    def select_result(self, item_name: str):
        result = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{item_name}")',
        )
        WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located(result)
        )
        self.driver.find_element(*result).click()
