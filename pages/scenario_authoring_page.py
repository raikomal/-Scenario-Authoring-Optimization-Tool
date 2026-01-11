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
        if isinstance(values, str):
            values = [values]

        container = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//label[normalize-space()='{label_text}']/following-sibling::div"
            ))
        )

        # Clear existing selections
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

    # -------------------------------------------------
    # DATE HANDLER
    # -------------------------------------------------
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
    # SCROLL + MOVE NETWORK GRAPH
    # -------------------------------------------------
    def scroll_and_move_network_graph(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.click()
        time.sleep(0.5)

        for _ in range(4):  # instead of 6
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)  # instead of 0.3

        print("✅ Wheel scroll executed")

        self.wait.until(EC.visibility_of_element_located(L.TOPOLOGY_VIEW_BTN))
        print("✅ Network section visible")

        actions = ActionChains(self.driver)
        actions.move_to_element(body) \
            .click_and_hold() \
            .move_by_offset(-150, 0) \
            .pause(0.2) \
            .move_by_offset(150, 0) \
            .release() \
            .perform()

        print("✅ Network graph drag simulated safely")

    # -------------------------------------------------
    # EDGE METRICS TABLE SCROLL
    # -------------------------------------------------
    def open_edge_metrics_and_scroll_table(self):
        print("➡ Opening Edge Metrics")

        self.wait.until(
            EC.element_to_be_clickable(L.EDGE_METRICS_BTN)
        ).click()

        time.sleep(1)

        table = self.wait.until(
            EC.visibility_of_element_located(L.EDGE_KPIS_SCROLL_CONTAINER)
        )

        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight;",
            table
        )
        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].scrollTop = 0;",
            table
        )
        time.sleep(1)

        print("✅ Edge KPIs table scrolled")

    # -------------------------------------------------
    # RUN OPTIMIZATION → CONFIGURATION & SOLVE
    # -------------------------------------------------
    def run_optimization_and_wait_for_config(self):
        print("➡ Switching to Configuration and Solve (guaranteed)")

        # 1️⃣ Click the TAB (not the button)
        tab = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Configuration and Solve']")
            )
        )
        self.driver.execute_script("arguments[0].click();", tab)

        # 2️⃣ HARD WAIT: TradeOff MUST mount
        print("⏳ Waiting for Configuration & Solve UI")
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//label[normalize-space()='Allocation Priority']")
            )
        )
        print("✅ Configuration & Solve fully mounted")

        # 3️⃣ NOW find Run Optimization
        run_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Run Optimization']")
            )
        )

        self.driver.execute_script("arguments[0].click();", run_btn)
        print("✅ Run Optimization clicked")

    def activate_configuration_and_solve_tab(self):
        print("➡ Activating Configuration and Solve tab (React state change)")

        tab = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH, "//button[normalize-space()='Configuration and Solve']"
            ))
        )

        # 🔥 Force React onClick (not normal click)
        self.driver.execute_script("""
            arguments[0].scrollIntoView({block:'center'});
            arguments[0].dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            arguments[0].dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
            arguments[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        """, tab)

        # 🔑 Wait for TradeOff component to MOUNT
        self.wait.until(
            EC.presence_of_element_located((
                By.XPATH, "//label[normalize-space()='Allocation Priority']"
            ))
        )

        print("✅ Configuration and Solve tab ACTIVE")

    def set_configuration_sliders(self, values):
        """
        Sets Configuration & Solve sliders safely
        values = [0.4, 0.3, 0.3, 0.3]
        """

        print("➡ Setting Configuration sliders")

        sliders = self.wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH, "//input[@type='range']"
            ))
        )

        assert len(sliders) >= len(values), "Not enough configuration sliders found"

        for i, value in enumerate(values):
            slider = sliders[i]

            self.driver.execute_script("""
                const slider = arguments[0];
                const value = arguments[1];

                slider.focus();
                slider.value = value;

                slider.dispatchEvent(new Event('input', { bubbles: true }));
                slider.dispatchEvent(new Event('change', { bubbles: true }));
            """, slider, value)

            time.sleep(0.3)

            print(f"✅ Configuration slider {i + 1} set to {value}")

    # -------------------------------------------------
    # MAIN FLOW
    # -------------------------------------------------
    def configure_sc_network_and_generate(self):

        # -------- PHASE 1: SC NETWORK SETUP --------
        self.select_react_dropdown("Facilities", ["PHX3"])
        self.select_react_dropdown("Supplier", ["Firebond", "JCI"])
        self.select_react_dropdown("Equipment Type", ["Generator w/ Enclosure"])

        self.set_start_date("2025-02-20")

        self.set_slider("Demand Multiplier", 0.60)
        self.set_slider("Time Steps", 11)
        self.set_slider("Days per period", 6)

        self.wait.until(EC.element_to_be_clickable(L.GENERATE_BUTTON)).click()
        print("✅ Generate & Visualize clicked")

        # ---- Phase 1 : Visualization ----

        # 1️⃣ Ensure Topology View is visible
        self.wait.until(EC.element_to_be_clickable(L.TOPOLOGY_VIEW_BTN)).click()
        print("🧭 Topology View activated")

        # 2️⃣ Light graph interaction (NO aggressive drag)
        self.scroll_and_move_network_graph()

        # 3️⃣ Open Edge Metrics
        self.open_edge_metrics_and_scroll_table()

        # 4️⃣ IMPORTANT: Return UI to neutral (Topology)
        self.wait.until(EC.element_to_be_clickable(L.TOPOLOGY_VIEW_BTN)).click()
        print("🔁 Returned to Topology View")

        print("🔒 Phase 1 complete — visualization stable")
        # ---- Phase 2 : Configuration ----
        self.run_optimization_and_wait_for_config()

        self.set_configuration_sliders([0.4, 0.3, 0.3, 0.3])

