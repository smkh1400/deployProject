from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

site_sentinels = {
    "https://ibcrowd.ir/opportunities/all": "div.col-md-6.col-xl-4.card-deck"
}

def loader_all_pages_combined(url, output_location):
    options = Options()
    # options.add_argument("--headless") //TODO: The project would not load if it is headless
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 20)

    combined_html_parts = []
    page = 1

    while True:
        print(f"Reading page {page}")

        # Wait for main content to load
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, site_sentinels[url])))
        except:
            print("Content didn't load. Stopping...")
            html_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
            combined_html_parts.append(f"<!-- Page {page} -->\n{html_content}")
            break

        # Save current page's HTML
        html_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        combined_html_parts.append(f"<!-- Page {page} -->\n{html_content}")

        try:
            # Wait for the "Next" button to be clickable
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Next"]')))
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
            next_li = next_button.find_element(By.XPATH, '..')  # Get the parent <li> to check for 'disabled'

            if 'disabled' in next_li.get_attribute("class"):
                print("Reached last page.")
                break

            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            print("waiting...")
            time.sleep(3)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    'a.page-link[aria-label="Next"]'
                ))
            )
            next_button.click()
            print("waiting for click")
            time.sleep(3)
            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"Pagination error: {e}")
            break

    driver.quit()

    # Combine and save HTML
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Combined Pages</title>
</head>
<body>
{''.join(combined_html_parts)}
</body>
</html>"""

    with open(output_location, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Saved output to {output_location}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html_loader.py <URL> <output file location>")
        sys.exit(1)

    url = sys.argv[1]
    output_file_location = sys.argv[2]

    loader_all_pages_combined(url, output_file_location)
