from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

site_sentinels = {
    "https://smartfunding.ir/projects": "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-10.muirtl-1o3bohy",
    "https://isatiscrowd.ir/planpage": "div.flex.flex-wrap.justify-center.mt-20.gap-6",
    "https://zeema.fund/crowdfunding-plan": "div.MuiGrid2-root.MuiGrid2-container.MuiGrid2-direction-xs-row.MuiGrid2-spacing-xs-2.mui-ijgs1b",
    "https://pulsar.ir/funds": "div.row.row-cols-1.row-cols-md-3.mb-3",
    "https://www.investorun.com/companies": "div.grid.grid-col-1.w-full.justify-items-center",
    "https://dongi.ir/discover": "div.projectItem.col-md-4.col-sm-6.col-xs-12"
}

def loader(url, output_location):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

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
    if (len(sys.argv) != 3):
        print("Usage: python html_loader.py <URL> <output file location>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file_location = sys.argv[2]

    loader(url, output_file_location)
