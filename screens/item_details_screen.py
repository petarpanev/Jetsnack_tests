from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


class ItemDetailsScreen:
    DETAILS_HEADING = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Details")',
    )

    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self, item_name: str):
        item_title = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{item_name}")',
        )
        wait = WebDriverWait(self.driver, Config.DEFAULT_TIMEOUT)
        wait.until(EC.visibility_of_element_located(self.DETAILS_HEADING))
        wait.until(EC.visibility_of_element_located(item_title))
        return True
