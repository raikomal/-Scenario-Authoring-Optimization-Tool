import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from pages.base_page import BasePage
from pages.scenario_authoring_locators import ScenarioAuthoringLocators as L


class ScenarioAuthoringPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)

    # 👇 ADD THIS METHOD ANYWHERE INSIDE THE CLASS
    def set_slider(self, label, value):
        slider = self.wait.until(
            EC.presence_of_element_located(L.SLIDER(label))
        )

        self.driver.execute_script(
            """
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            slider,
            value
        )

        print(f"✅ {label} slider set to {value}")


    # -------------------------------------------------
    # PAGE LOAD VALIDATION
    # -------------------------------------------------
    def validate_page_loaded(self):
        self.wait.until(EC.visibility_of_element_located(L.PAGE_ROOT))
        print("✅ Scenario Authoring page loaded (layout + header confirmed)")

    # -------------------------------------------------
    # REACT SELECT (PLAYWRIGHT-LIKE BEHAVIOR)
    # -------------------------------------------------
    def select_react_dropdown(self, label_text, values):
        """
        Stable React-Select handler
        - Clears old values
        - Selects fresh values
        - Works across reruns
        """

        if isinstance(values, str):
            values = [values]

        # Locate field container using label
        container = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//label[normalize-space()='{label_text}']/following-sibling::div"
            ))
        )

        # 🔴 CLEAR EXISTING CHIPS (critical fix)
        clear_icons = container.find_elements(
            By.XPATH, ".//*[name()='svg' and @aria-hidden='true']"
        )
        for icon in clear_icons:
            try:
                icon.click()
                time.sleep(0.2)
            except:
                pass

        # Focus actual input
        input_box = container.find_element(By.XPATH, ".//input")
        input_box.click()
        time.sleep(0.3)

        # Select values
        for value in values:
            input_box.send_keys(value)
            time.sleep(0.4)
            input_box.send_keys(Keys.ENTER)
            time.sleep(0.4)

        print(f"✅ Selected {values} in {label_text}")

    # # -------------------------------------------------
    # # SLIDER HANDLER
    # # -------------------------------------------------
    # def set_slider(self, locator, value):
    #     slider = self.wait.until(EC.element_to_be_clickable(locator))
    #     self.driver.execute_script(
    #         "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
    #         slider, value
    #     )

    # -------------------------------------------------
    # MAIN FLOW
    # -------------------------------------------------
    def configure_sc_network_and_generate(self):

        # ----------- DROPDOWNS -----------
        self.select_react_dropdown("Facilities", ["PHX3"])
        self.select_react_dropdown("Supplier", ["Firebond", "JCI"])
        self.select_react_dropdown("Equipment Type", ["Generator w/ Enclosure"])

        # ----------- START DATE -----------
        start_date = self.wait.until(EC.element_to_be_clickable(L.START_DATE))
        start_date.clear()
        start_date.send_keys("2025-06-12")
        print("✅ Start date set")

        # ---------- SLIDERS (ADD HERE) ----------
        self.set_slider("Demand Multiplier", 0.60)
        self.set_slider("Time Steps", 11)
        self.set_slider("Days per period", 6)

        # ----------- GENERATE -----------
        self.wait.until(EC.element_to_be_clickable(L.GENERATE_BUTTON)).click()
        print("✅ Generate & Visualize clicked")
