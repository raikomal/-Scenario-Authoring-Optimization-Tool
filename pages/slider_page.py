from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class SliderPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def click_slider_button(self, name: str):
        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[normalize-space()='{name}']")
            )
        )
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)   # IMPORTANT: React state settle

    def navigate_to_part_allocation(self):
        """
        Demand → Capacity → Supply → Part Allocation
        """
        self.click_slider_button("Demand Insights")
        self.click_slider_button("Capacity Insights")
        self.click_slider_button("Supply Insights")
        self.click_slider_button("Part Allocation Insights")

        # ❌ DO NOT wait for any element here
        # ✅ Just give React time
        time.sleep(2)

    def open_scenario_authoring_tool(self):
        """
        Slider sequence → Scenario Authoring
        """
        self.navigate_to_part_allocation()

        scenario_card = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'dashboard-card')]"
                    "[.//div[contains(normalize-space(),'Scenario Authoring')]]"
                )
            )
        )

        self.driver.execute_script("arguments[0].click();", scenario_card)
        time.sleep(3)

    # slider_page.py

    def hover_and_click_scenario_authoring_tool(self):
        """
        FINAL & CORRECT:
        Click Scenario Authoring via dashboard-card index
        """

        # 1️⃣ Ensure Part Allocation tab
        self.navigate_to_part_allocation()
        time.sleep(3)

        # 2️⃣ Scope to Part Allocation container (IMPORTANT)
        part_allocation_section = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//button[normalize-space()='Part Allocation Insights']/ancestor::div"
            ))
        )

        # 3️⃣ Find all cards INSIDE Part Allocation
        cards = part_allocation_section.find_elements(
            By.XPATH,
            ".//div[contains(@class,'dashboard-card') and contains(@class,'cursor-pointer')]"
        )

        print(f"🔍 Part Allocation cards found: {len(cards)}")

        if len(cards) < 3:
            raise Exception("❌ Scenario Authoring card not rendered")

        scenario_card = cards[2]  # ✅ 3rd card

        # 4️⃣ Scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            scenario_card
        )
        time.sleep(1)

        # 5️⃣ Hover (activate animation)
        ActionChains(self.driver).move_to_element(scenario_card).pause(0.5).perform()

        # 6️⃣ JS click (React-safe)
        self.driver.execute_script("arguments[0].click();", scenario_card)
        time.sleep(4)

        print("✅ Scenario Authoring card clicked")
