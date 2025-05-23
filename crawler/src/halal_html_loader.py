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
    "https://halalfund.ir/projects": "div.ant-row.homeProjectsWrapper"
}

SCROLL_PAUSE_TIME = 10
MAX_TRIES_WITH_NO_NEW_CONTENT = 2

def loader(url, output_location):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--log-level=3")  # Fatal only

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                site_sentinels[url]
            ))
        )
    except:
        print("Projects didn't load. Terminating...")
        return
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    tries = 0
    previous_item_count = 0
    
    while tries < MAX_TRIES_WITH_NO_NEW_CONTENT:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        print("Scrolling...")

        items = driver.find_elements(By.CSS_SELECTOR, "div.ant-col.ProjectItemWrapper.ant-col-xs-24.ant-col-sm-12.ant-col-md-12.ant-col-lg-8.ant-col-xl-8")
        current_item_count = len(items)
        print(f"current item count is {current_item_count}")

        if current_item_count == previous_item_count:
            tries += 1
        else:
            tries = 0
        
        previous_item_count = current_item_count

    html_content = driver.page_source
    with open(output_location, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Saved output to {output_location}")

    driver.quit()


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Usage: python html_loader.py <URL> <output file location>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file_location = sys.argv[2]

    loader(url, output_file_location)
