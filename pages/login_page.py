from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginPage:
    """
    Stable Login Page Object
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    # ---------------- LOCATORS ----------------
    USERNAME = "//input[@placeholder='Username or email']"
    PASSWORD = "//input[@placeholder='Password']"
    LOGIN_BTN = "//button[normalize-space()='LOGIN']"

    # ---------------- ACTIONS ----------------
    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.USERNAME))).clear()
        self.driver.find_element(By.XPATH, self.USERNAME).send_keys(username)

        self.driver.find_element(By.XPATH, self.PASSWORD).clear()
        self.driver.find_element(By.XPATH, self.PASSWORD).send_keys(password)

        self.driver.find_element(By.XPATH, self.LOGIN_BTN).click()

        # Dashboard loaded
        self.wait.until(EC.url_contains("microdashboard"))
        time.sleep(2)
        print("✅ Login successful, dashboard loaded")
