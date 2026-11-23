import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.config import Config


@pytest.fixture
def driver():
    options = UiAutomator2Options().load_capabilities(Config.ANDROID_CAPS)
    session = webdriver.Remote(
        command_executor=Config.APPIUM_SERVER_URL,
        options=options,
    )
    try:
        yield session
    finally:
        session.quit()
