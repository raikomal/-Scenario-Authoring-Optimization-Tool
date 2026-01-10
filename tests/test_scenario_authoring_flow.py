import pytest
from pages.login_page import LoginPage
from pages.slider_page import SliderPage
from pages.scenario_authoring_page import ScenarioAuthoringPage
from utils.ui_report_writer import start_new_report, write_test_report


@pytest.mark.e2e
def test_scenario_authoring_full_flow(driver):

    start_new_report()
    task_id = 1

    # LOGIN
    LoginPage(driver).login("user@gmail.com", "12345")

    write_test_report(
        "Tower Track", "Web", "Login",
        "Valid Login",
        "Login with valid credentials",
        "Enter username and password",
        "User should login successfully",
        "User logged in",
        "Pass", "", task_id
    )
    task_id += 1

    # NAVIGATION
    SliderPage(driver).hover_and_click_scenario_authoring_tool()

    write_test_report(
        "Tower Track", "Part Allocation Insights", "Navigation",
        "Navigate to Scenario Authoring Tool",
        "Open Scenario Authoring & Optimization Tool",
        "Click Scenario Authoring card",
        "Page should open",
        "Page opened",
        "Pass", "", task_id
    )
    task_id += 1

    # PAGE VALIDATION
    scenario_page = ScenarioAuthoringPage(driver)
    scenario_page.validate_page_loaded()

    write_test_report(
        "Tower Track", "Part Allocation Insights",
        "Scenario Authoring & Optimization Tool",
        "Verify Page Load",
        "Ensure Scenario Authoring page loads correctly",
        "Open Scenario Authoring tool",
        "Scenario Authoring page should load",
        "Page loaded successfully",
        "Pass", "", task_id
    )
