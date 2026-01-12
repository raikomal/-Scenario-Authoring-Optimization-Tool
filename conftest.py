import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.ui_report_writer import write_fail_report


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    # ✅ Selenium Manager (NO webdriver-manager)
    driver = webdriver.Chrome(options=options)
    driver.get("http://103.204.95.212:8084")

    yield driver
    driver.quit()


# =========================
# AUTO FAIL REPORT HOOK
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            write_fail_report(
                title=f"Test Failed: {item.name}",
                error_message=str(rep.longrepr)
            )
        except Exception as e:
            # NEVER break pytest because of reporting
            print("⚠️ Fail report generation error:", e)
