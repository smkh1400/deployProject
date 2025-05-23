from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

site_sentinels = {
    "https://novincrowd.ir/projects": "div.col-lg-4.col-md-6"
}

def loader_all_pages_combined(url, output_location):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    combined_html_parts = []
    page = 1

    while True:
        full_url = f"{url}?page={page}"
        print(f"Loading {full_url}")
        driver.get(full_url)


        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    site_sentinels[url]
                ))
            )
        except:
            print("Projects didn't load. Terminating...")
            break

        html_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        combined_html_parts.append(f"<!-- Page {page} -->\n{html_content}")
        page += 1

    driver.quit()

    full_html = f"""<!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>Combined NovinCrowd Pages </title>
                        </head>
                        <body>
                            {''.join(combined_html_parts)}
                        </body>
                    </html>"""
    
    with open(output_location, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Saved output to {output_location}")



if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Usage: python html_loader.py <URL> <output file location>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file_location = sys.argv[2]

    loader_all_pages_combined(url, output_file_location)
