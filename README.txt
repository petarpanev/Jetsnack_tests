Jetsnack Appium test project
============================

This project uses Python, pytest, and Appium's UiAutomator2 driver to smoke-test
apps/app-debug.apk. Android screen locators belong in the screens/ package.

Prerequisites
-------------

- Python 3.9 or newer
- Node.js and Appium 2
- Appium's UiAutomator2 driver (`appium driver install uiautomator2`)
- Android SDK platform-tools and an Android emulator or connected device

If Appium is not installed yet, install it and its Android driver:

    npm install --global appium
    appium driver install uiautomator2

Python setup
------------

Create and activate a virtual environment, then install the project dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

Run Appium in a separate terminal:

    appium

Start an Android emulator or connect a device, then run:

    pytest

Configuration
-------------

Configuration is loaded from the project-root .env file. APP_PATH defaults to
apps/app-debug.apk; relative paths are resolved from the project root. Optional
settings are APPIUM_SERVER_URL, DEFAULT_TIMEOUT, PLATFORM_NAME,
AUTOMATION_NAME, DEVICE_NAME, UDID, APP_PACKAGE, APP_ACTIVITY, and NO_RESET.
The Jetsnack package and launch activity are used by default. Keep local
configuration and secrets in .env; it is excluded from version control.

Screen objects and locators
---------------------------

Put each screen's selectors in its screen class under screens/. Add tests under
tests/ and share the Appium session through the driver fixture in tests/conftest.py.
