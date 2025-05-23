from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

LOGIN_URL = "https://cfrazavi.ir/auth/login_password/"
USERNAME = 3861397625
PASSWORD = "Aa12345678@"

def login(driver):
    driver.get(LOGIN_URL)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.auth-form"
            ))
        )

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.CLASS_NAME, "login-btn")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CLASS_NAME,
                "login-btn"
            ))
        )

        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.row.g-32.mb-32"
            ))
        )

        print("Login successful.")

    except Exception as e:
        print(f"login failed: {e}")
        driver.quit()
        sys.exit(1)



def loader(output_location):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    login(driver)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "div.row.g-32.mb-32"
            ))
        )
    except Exception as e:
        print(f"Exception occurred: {e}")
        print("Projects didn't load. Terminating...")
        return

    html_content = driver.page_source
    with open(output_location, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Saved output to {output_location}")

    driver.quit()


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f"Usage: python {sys.argv[0]} <output file location>")
        sys.exit(1)
    
    output_file_location = sys.argv[1]

    loader(output_file_location)
