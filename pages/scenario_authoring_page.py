from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ScenarioAuthoringPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def validate_page_loaded(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h1[contains(text(),'Scenario Authoring')]")
            )
        )
