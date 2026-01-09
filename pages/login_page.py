from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    # =========================
    # LOGIN ACTION
    # =========================
    def login(self, username, password):
        username_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))
        )
        password_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))
        )

        username_input.clear()
        username_input.send_keys(username)

        password_input.clear()
        password_input.send_keys(password)

        login_button.click()

        # Post-login assertion
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Micro-Apps')]")
            )
        )
