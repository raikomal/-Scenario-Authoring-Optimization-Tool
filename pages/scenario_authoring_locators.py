from selenium.webdriver.common.by import By


class ScenarioAuthoringLocators:

    # ---------------- PAGE LOAD ----------------
    PAGE_ROOT = (
        By.XPATH,
        "//div[normalize-space()='Supply Chain Network Configuration']"
    )

    # ---------------- DATE ----------------
    START_DATE = (
        By.XPATH,
        "//label[normalize-space()='Start Date']/following::input[1]"
    )

    # ---------------- SLIDERS ----------------
    @staticmethod
    def SLIDER(label):
        return (
            By.XPATH,
            f"//label[normalize-space()='{label}']/following::input[@type='range'][1]"
        )

    # ---------------- ACTION ----------------
    GENERATE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Generate & Visualize Supply Chain Network']"
    )

    # ---------------- NETWORK ----------------
    NETWORK_OVERVIEW_CONTAINER = (
        By.XPATH,
        "//div[.//div[normalize-space()='Network Overview']]"
    )



    NETWORK_GRAPH_RENDERER = (
        By.CSS_SELECTOR,
        ".react-flow__renderer"
    )

    TOPOLOGY_VIEW_BTN = (
        By.XPATH,
        "//button[normalize-space()='Topology View']"
    )

    EDGE_METRICS_BTN = (
        By.XPATH,
        "//button[normalize-space()='Edge Metrics']"
    )
    EDGE_KPIS_SCROLL_CONTAINER = (
        By.XPATH,
        "//h2[normalize-space()='Edge Kpis']"
        "/following::div[contains(@class,'overflow-y-auto')][1]"
    )

