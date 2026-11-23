from config.config import Config
from screens.home_screen import HomeScreen


def test_app_launches_to_home_screen(driver):
    assert driver.current_package == Config.APP_PACKAGE
    assert HomeScreen(driver).wait_until_loaded()
