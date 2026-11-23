from datetime import datetime
from pathlib import Path
import re

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.config import Config, PROJECT_ROOT


def pytest_sessionstart(session):
    session.config._test_result_timestamp = datetime.now().astimezone()
    session.config._test_result_records = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    records = item.config._test_result_records
    record = records.setdefault(
        item.nodeid,
        {"phases": [], "screenshot": None, "screenshot_error": None},
    )
    record["phases"].append(
        (
            report.when,
            report.outcome,
            report.longreprtext if report.failed else None,
        )
    )

    if report.failed and record["screenshot"] is None and not record["screenshot_error"]:
        driver = item.funcargs.get("driver")
        if driver is None:
            record["screenshot_error"] = (
                "Screenshot unavailable: the Appium driver was not initialized."
            )
            return

        screenshot_dir = PROJECT_ROOT / "results" / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", item.nodeid).strip("_")
        screenshot_path = screenshot_dir / f"{slug}.png"
        try:
            if driver.get_screenshot_as_file(str(screenshot_path)):
                record["screenshot"] = screenshot_path.relative_to(
                    PROJECT_ROOT / "results"
                )
            else:
                record["screenshot_error"] = (
                    "Screenshot capture returned no image."
                )
        except Exception as error:
            record["screenshot_error"] = (
                f"Screenshot capture failed: {type(error).__name__}: {error}"
            )


def pytest_sessionfinish(session, exitstatus):
    results_dir = PROJECT_ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = session.config._test_result_timestamp
    results_path = results_dir / f"test-results-{timestamp:%Y%m%d-%H%M%S-%f}.md"
    records = session.config._test_result_records

    statuses = {}
    for nodeid, record in records.items():
        outcomes = [outcome for _, outcome, _ in record["phases"]]
        if "failed" in outcomes:
            status = "FAILED"
        elif "skipped" in outcomes:
            status = "SKIPPED"
        else:
            status = "PASSED"
        statuses[nodeid] = status

    counts = {
        status: sum(result == status for result in statuses.values())
        for status in ("PASSED", "FAILED", "SKIPPED")
    }
    lines = [
        "# Test Results",
        "",
        f"- Started: {timestamp.isoformat(timespec='seconds')}",
        f"- Finished: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"- Summary: {counts['PASSED']} passed, {counts['FAILED']} failed, "
        f"{counts['SKIPPED']} skipped",
        "",
    ]

    for status in ("PASSED", "FAILED", "SKIPPED"):
        lines.extend((f"## {status.title()} tests", ""))
        matching = [
            (nodeid, record)
            for nodeid, record in records.items()
            if statuses[nodeid] == status
        ]
        if not matching:
            lines.extend(("_None._", ""))
            continue

        for nodeid, record in matching:
            lines.append(f"- **{nodeid}** — {status}")
            if status == "FAILED":
                for phase, outcome, reason in record["phases"]:
                    if outcome == "failed":
                        lines.extend(
                            (
                                f"  - Reason ({phase}):",
                                "",
                                *[f"    {line}" for line in reason.splitlines()],
                            )
                        )
                if record["screenshot"] is not None:
                    lines.append(
                        f"  - Screenshot: `{record['screenshot'].as_posix()}`"
                    )
                elif record["screenshot_error"]:
                    lines.append(f"  - {record['screenshot_error']}")
            lines.append("")

    results_path.write_text("\n".join(lines), encoding="utf-8")
    session.config._test_result_path = results_path


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
        try:
            session.terminate_app(Config.APP_PACKAGE)
        finally:
            session.quit()
