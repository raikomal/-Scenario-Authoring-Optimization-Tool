from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SliderPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.actions = ActionChains(driver)

    # =====================================================
    # SCENARIO AUTHORING & OPTIMIZATION TOOL
    # =====================================================
    def open_scenario_authoring_tool(self):
        """
        Hover and click on Scenario Authoring & Optimization Tool card
        """

        scenario_card = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(text(),'Scenario Authoring & Optimization Tool')]"
            ))
        )

        self.actions.move_to_element(scenario_card).pause(0.3).click().perform()

        # Assert landing page loaded
        self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//h1[contains(text(),'Hitachi Tower Track')]"
            ))
        )
