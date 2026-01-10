from selenium.webdriver.common.by import By


class ScenarioAuthoringLocators:

    @staticmethod
    def SLIDER(label):
        return (
            By.XPATH,
            f"//label[normalize-space()='{label}']/following::input[@type='range'][1]"
        )

    # PAGE LOAD CHECK
    PAGE_ROOT = (
        By.XPATH,
        "//div[contains(@class,'text-gray-100') and contains(text(),'Supply')]"
    )

    # DATE
    START_DATE = (
        By.XPATH,
        "//label[normalize-space()='Start Date']/following::input[1]"
    )

    # SLIDERS
    DEMAND_MULTIPLIER = (
        By.XPATH,
        "//label[normalize-space()='Demand Multiplier']/following::input[@type='range'][1]"
    )

    TIME_STEPS = (
        By.XPATH,
        "//label[normalize-space()='Time Steps']/following::input[@type='range'][1]"
    )

    DAYS_PER_PERIOD = (
        By.XPATH,
        "//label[normalize-space()='Days per period']/following::input[@type='range'][1]"
    )

    # ACTION
    GENERATE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Generate & Visualize Supply Chain Network']"
    )
