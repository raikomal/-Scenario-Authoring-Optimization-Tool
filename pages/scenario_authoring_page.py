import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

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

    def verify_configuration_loaded(self):
        print("🔎 Verifying Configuration & Solve content")

        self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[normalize-space()='Allocation Priority']"
            ))
        )

        print("✅ Configuration & Solve UI confirmed")

    def scroll_to_cost_breakdown_optimized(self):
        print("⬇ Scrolling to Cost Breakdown (Optimized)")

        # 🔑 Ensure charts exist first
        self.wait_for_optimization_results()

        header = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//h2[contains(normalize-space(),'Cost Breakdown')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            header
        )

        time.sleep(1)
        print("✅ Cost Breakdown (Optimized) visible")

    def hover_cost_breakdown_chart(self):
        print("🟡 Hovering Cost Breakdown bars")

        bars = self.wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//div[contains(@id,'highcharts')]//*[name()='path']"
            ))
        )

        for bar in bars[:5]:  # limit to first few bars
            self.driver.execute_script("""
                arguments[0].dispatchEvent(
                    new MouseEvent('mouseover', { bubbles: true })
                );
            """, bar)
            time.sleep(0.4)

        print("✅ Cost Breakdown hover completed")

    def scroll_cost_breakdown_summary_and_return(self):
        print("⬇ Scrolling to Cost Breakdown Summary")

        summary = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//h2[normalize-space()='Cost Breakdown Summary']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            summary
        )

        time.sleep(1)

        print("⬆ Returning to Run Optimization")

        run_btn = self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//button[normalize-space()='Run Optimization']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            run_btn
        )

        time.sleep(1)
        print("✅ Returned to Run Optimization")

    def scroll_configuration_container(self):
        print("⬇ Scrolling Configuration & Solve container")

        container = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'overflow-y-auto')]"
            ))
        )

        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            container
        )
        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].scrollTop = 0",
            container
        )

        print("✅ Configuration container scroll completed")

    def wait_for_optimization_results(self):
        print("⏳ Waiting for Optimization results (charts)")

        self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@id,'highcharts')]//*[name()='svg']"
            ))
        )

        print("✅ Optimization charts rendered")

    def hover_cost_breakdown_optimized(self):
        print("🟡 Hovering Cost Breakdown (Optimized) bars — stable")

        bars = self.wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//div[contains(@id,'highcharts')]//*[name()='path' and contains(@class,'highcharts-point')]"
            ))
        )

        actions = ActionChains(self.driver)

        hover_count = min(4, len(bars))  # 🔑 allow up to 4 safely

        for idx, bar in enumerate(bars[:hover_count], start=1):
            actions.move_to_element(bar).pause(0.8).perform()
            print(f"✅ Hovered bar {idx}")
            time.sleep(0.5)

        print("✅ Cost Breakdown hover sequence completed (Highcharts-safe)")

    def scroll_edge_kpis_table_real(self):
        print("⬇ Scrolling Edge KPIs table (REAL internal scroll)")

        table_container = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//h2[normalize-space()='Edge Kpis']"
                "/following::div[contains(@class,'overflow-y-auto')][1]"
            ))
        )

        # Bring table into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            table_container
        )
        time.sleep(0.8)

        # 🔑 REAL internal scrolling
        for step in range(4):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].clientHeight;",
                table_container
            )
            print(f"➡ KPI scroll step {step + 1}")
            time.sleep(0.7)

        print("✅ Edge KPIs table ACTUALLY scrolled internally")

        scroll_pos = self.driver.execute_script(
            "return arguments[0].scrollTop;",
            table_container
        )
        assert scroll_pos > 0, "❌ Edge KPIs table did NOT scroll internally"

    def stabilize_view_after_hover(self):
        print("🧘 Stabilizing view after hover")

        self.driver.execute_script("""
            const x = window.scrollX;
            const y = window.scrollY;
            window.scrollTo(x, y);
        """)

        time.sleep(1)  # allow layout to settle

    def switch_to_granular_view(self):
        print("⬆ Preparing to switch to Granular View")

        # ✅ 1. If already in Granular View, SKIP
        current_url = self.driver.current_url
        if "granule_view" in current_url:
            print("ℹ Already in Granular View — skipping toggle click")
            return

        # 2️⃣ Scroll to top (visual safety)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)

        # 3️⃣ Find and click Granular View toggle
        granular_btn = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//button[normalize-space()='Granular View']"
            ))
        )

        self.driver.execute_script("arguments[0].click();", granular_btn)
        print("➡ Granular View clicked")

        # 4️⃣ Wait for route change
        self.wait.until(EC.url_contains("/granule_view"))
        print("🌐 URL updated to /granule_view")

        # 5️⃣ HARD page verification
        self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//h2[normalize-space()='Scenario Controls']"
            ))
        )
        print("✅ Granular View fully loaded and ready")

    def select_granular_source_and_target(self):
        print("🎯 Selecting Granular Source & Target nodes (FINAL + AUTO SCROLL)")

        # Wait for Granular page
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[normalize-space()='Scenario Controls']")
            )
        )

        # ======================
        # SOURCE NODE (React-safe)
        # ======================
        source_select = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//label[normalize-space()='Source Node :']/following-sibling::select"
            ))
        )

        self.driver.execute_script("""
            arguments[0].value = 'DC-Chicago';
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, source_select)

        time.sleep(1)

        # ======================
        # TARGET NODE (depends on Source)
        # ======================
        target_select = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//label[normalize-space()='Target Node :']/following-sibling::select"
            ))
        )

        self.driver.execute_script("""
            arguments[0].value = 'Lane-West';
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, target_select)

        time.sleep(1)

        print("✅ Source Node selected: DC-Chicago")
        print("✅ Target Node selected: Lane-West")

        # ======================
        # FULL SCROLL FOR GENERATED DATA
        # ======================
        self.scroll_granular_results_fully()

    def adjust_granular_sliders(self):
        print("🎚 Adjusting Granular sliders (VISIBLE & STABLE)")

        sliders = {
            "OTIF Target": 0.98,
            "Max Expedite (% of flow)": 0.21,
            "Max Avg Lateness (periods)": 1.5,
            "Utilization Target": 0.96,
            "Cost Pressure": 0.8
        }

        for label, value in sliders.items():
            slider = self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//label[contains(normalize-space(),'{label}')]/following::input[@type='range'][1]"
                ))
            )

            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, slider, value)

            print(f"✅ {label} set to {value}")
            time.sleep(0.3)

        print("🎉 Granular sliders configured")

    def scroll_granular_results_fully(self):
        print("⬇ Scrolling Granular results container FULLY")

        self.driver.execute_script("""
            const container = document.querySelector("div.mt-4");
            if (container) {
                container.scrollTop = container.scrollHeight;
            } else {
                window.scrollTo(0, document.body.scrollHeight);
            }
        """)

        time.sleep(1)
        print("✅ Granular data scrolled fully into view")

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

        print("Phase 1 complete — visualization stable")
        # ---- Phase 2 : Configuration ----
        self.run_optimization_and_wait_for_config()
        self.verify_configuration_loaded()

        self.set_configuration_sliders([0.4, 0.3, 0.3, 0.3])

        self.scroll_configuration_container()
        # Cost Breakdown section
        self.scroll_to_cost_breakdown_optimized()
        self.hover_cost_breakdown_optimized()
        self.stabilize_view_after_hover()

        # Edge KPIs LAST
        self.scroll_edge_kpis_table_real()

        self.switch_to_granular_view()








