import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.scenario_authoring_locators import ScenarioAuthoringLocators as L


class ScenarioAuthoringPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    # -------------------------------------------------
    # PAGE LOAD VALIDATION
    # -------------------------------------------------
    def validate_page_loaded(self):
        self.wait.until(EC.visibility_of_element_located(L.PAGE_ROOT))
        print("✅ Scenario Authoring page loaded (layout + header confirmed)")

    # -------------------------------------------------
    # REACT SELECT DROPDOWN HANDLER
    # -------------------------------------------------
    def select_react_dropdown(self, label_text, values):
        """
        Stable React-Select handler:
        - Clears old values
        - Selects fresh values
        """

        if isinstance(values, str):
            values = [values]

        container = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//label[normalize-space()='{label_text}']/following-sibling::div"
            ))
        )

        # Clear existing chips
        clear_icons = container.find_elements(
            By.XPATH, ".//*[name()='svg' and @aria-hidden='true']"
        )
        for icon in clear_icons:
            try:
                icon.click()
                time.sleep(0.2)
            except:
                pass

        input_box = container.find_element(By.XPATH, ".//input")
        input_box.click()
        time.sleep(0.3)

        for value in values:
            input_box.send_keys(value)
            time.sleep(0.4)
            input_box.send_keys(Keys.ENTER)
            time.sleep(0.4)

        print(f"✅ Selected {values} in {label_text}")

    # -------------------------------------------------
    # SLIDER HANDLER (REACT SAFE)
    # -------------------------------------------------
    def set_slider(self, label, value):
        slider = self.wait.until(
            EC.presence_of_element_located(L.SLIDER(label))
        )

        self.driver.execute_script(
            """
            const slider = arguments[0];
            const value = arguments[1];

            slider.focus();
            slider.value = value;

            slider.dispatchEvent(new Event('input', { bubbles: true }));
            slider.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            slider,
            value
        )

        time.sleep(0.3)
        print(f"✅ {label} slider set to {value}")

    def set_start_date(self, date_value):
        date_input = self.wait.until(
            EC.presence_of_element_located(L.START_DATE)
        )

        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];

            input.focus();
            input.value = value;

            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            date_input,
            date_value
        )

        print(f"✅ Start date set to {date_value}")

    # -------------------------------------------------
    # SCROLL + MOVE REACT FLOW NETWORK GRAPH
    # -------------------------------------------------
    def scroll_and_move_network_graph(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.click()
        time.sleep(0.5)

        # 1️⃣ Scroll down like real user
        for _ in range(6):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        print("✅ Wheel scroll executed")

        # 2️⃣ Graph render signal
        self.wait.until(EC.visibility_of_element_located(L.TOPOLOGY_VIEW_BTN))
        print("✅ Network section visible")

        time.sleep(1)

        # 3️⃣ SAFE drag (small bounded movement)
        actions = ActionChains(self.driver)

        actions.move_to_element(body) \
            .click_and_hold() \
            .move_by_offset(-150, 0) \
            .pause(0.2) \
            .move_by_offset(150, 0) \
            .release() \
            .perform()

        print("✅ Network graph drag simulated safely")

    def open_edge_metrics_and_scroll_table(self):
        print("➡ Opening Edge Metrics")

        # Click Edge Metrics button
        self.wait.until(
            EC.element_to_be_clickable(L.EDGE_METRICS_BTN)
        ).click()

        time.sleep(2)

        # Locate Edge KPIs scrollable table
        table = self.wait.until(
            EC.visibility_of_element_located(L.EDGE_KPIS_SCROLL_CONTAINER)
        )

        # Scroll DOWN inside table
        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight;",
            table
        )
        time.sleep(2)

        # Scroll UP inside table
        self.driver.execute_script(
            "arguments[0].scrollTop = 0;",
            table
        )
        time.sleep(1)

        print("✅ Edge KPIs table scrolled")

    # -------------------------------------------------
    # MAIN FLOW
    # -------------------------------------------------
    def configure_sc_network_and_generate(self):

        # ----------- DROPDOWNS -----------
        self.select_react_dropdown("Facilities", ["PHX3"])
        self.select_react_dropdown("Supplier", ["Firebond", "JCI"])
        self.select_react_dropdown("Equipment Type", ["Generator w/ Enclosure"])

        # ----------- START DATE -----------
        self.set_start_date("2025-02-20")

        # ----------- SLIDERS -----------
        self.set_slider("Demand Multiplier", 0.60)
        self.set_slider("Time Steps", 11)
        self.set_slider("Days per period", 6)

        # Generate
        self.wait.until(EC.element_to_be_clickable(L.GENERATE_BUTTON)).click()
        print("✅ Generate & Visualize clicked")

        # Graph render signal (THIS is your wait)
        self.wait.until(EC.visibility_of_element_located(L.TOPOLOGY_VIEW_BTN))
        self.wait.until(EC.visibility_of_element_located(L.EDGE_METRICS_BTN))
        print("✅ Network view buttons visible")

        time.sleep(1)

        # Scroll + move (NO graph lookup)
        self.scroll_and_move_network_graph()

        self.open_edge_metrics_and_scroll_table()



