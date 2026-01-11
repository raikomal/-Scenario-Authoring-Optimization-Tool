from selenium.webdriver.common.by import By


class ScenarioAuthoringLocators:

    # ================= PAGE LOAD =================
    PAGE_ROOT = (
        By.XPATH,
        "//div[normalize-space()='Supply Chain Network Configuration']"
    )

    # ================= DATE =================
    START_DATE = (
        By.XPATH,
        "//label[normalize-space()='Start Date']/following::input[1]"
    )

    # ================= SLIDERS =================
    @staticmethod
    def SLIDER(label):
        return (
            By.XPATH,
            f"//label[normalize-space()='{label}']/following::input[@type='range'][1]"
        )

    # ================= ACTION =================
    GENERATE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Generate & Visualize Supply Chain Network']"
    )

    # ================= NETWORK =================
    TOPOLOGY_VIEW_BTN = (
        By.XPATH,
        "//button[normalize-space()='Topology View']"
    )

    EDGE_METRICS_BTN = (
        By.XPATH,
        "//button[normalize-space()='Edge Metrics']"
    )

    # ================= EDGE KPIs TABLE =================
    EDGE_KPIS_SCROLL_CONTAINER = (
        By.XPATH,
        "//h2[contains(translate(., 'KPIS', 'kpis'), 'kpis')]"
        "/following::div[contains(@class,'overflow-y-auto')][1]"
    )

    # ================= CONFIGURATION & SOLVE =================
    CONFIGURATION_SOLVE_BTN = (
        By.XPATH,
        "//button[normalize-space()='Configuration and Solve']"
    )

    RUN_OPTIMIZATION_BTN = (
        By.XPATH,
        "//button[normalize-space()='Run Optimization']"
    )

    # React TradeOff component mount signal
    TRADEOFF_ROOT = (
        By.XPATH,
        "//label[normalize-space()='Allocation Priority']"
    )
