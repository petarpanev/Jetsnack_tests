import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


def _project_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


class Config:
    APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    APP_PATH = _project_path(
        os.getenv("APP_PATH", "apps/app-debug.apk")
    )
    APP_PACKAGE = os.getenv("APP_PACKAGE", "com.example.jetsnack")
    APP_ACTIVITY = os.getenv(
        "APP_ACTIVITY", "com.example.jetsnack.ui.MainActivity"
    )

    ANDROID_CAPS = {
        "platformName": os.getenv("PLATFORM_NAME", "Android"),
        "appium:automationName": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
        "appium:deviceName": os.getenv("DEVICE_NAME", "Android Emulator"),
        "appium:noReset": _str_to_bool(os.getenv("NO_RESET", "false")),
        "appium:app": str(APP_PATH),
        "appium:appPackage": APP_PACKAGE,
        "appium:appActivity": APP_ACTIVITY,
    }

    if os.getenv("UDID"):
        ANDROID_CAPS["appium:udid"] = os.getenv("UDID")
