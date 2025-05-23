#TODO: needs refactoring
from bs4 import BeautifulSoup
import requests
from data import ProjectData

import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://smartfunding.ir/"

platform_data = {
    "name": "smartfunding",
    "link": crowdfunding_link
}

def crawler(html_path, result_path):
    platform_response = requests.post(f"{API_BASE_URL}/platforms/", json=platform_data)
    if platform_response.status_code in [200, 201]:
        print("Crowdfunding platform posted.")
    else:
        print("Failed to post crowdfunding platform:", platform_response.text)

    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    resultFile = open(result_path, "w", encoding="utf-8")

    elements = soup.find_all("div", class_="MuiCardContent-root muirtl-1qw96cp")

    for idx, element in enumerate(elements, start = 1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        project.project_name = element.find_all('p')[0].get_text(strip=True)

        informations = element.find_all("div", style="margin: 10px 0px; display: flex; justify-content: space-between;")

        needed_fund = None
        funded_amount = None
        
        for div in informations:
            first_p = div.find('p')
            if first_p:
                if first_p.get_text(strip=True) == "متقاضی:":
                    project.company_title = div.find_all("p")[1].get_text(strip=True)
                if first_p.get_text(strip=True) == "سود پیشبینی شده طرح:":
                    estimated_profit = div.find_all("p")[1].get_text(strip=True)
                    project.estimated_profit = float(estimated_profit.replace("%", "")) if estimated_profit is not None else -1
                if first_p.get_text(strip=True) == "مبلغ مورد نیاز طرح:":
                    needed_fund = div.find_all("p")[1].get_text(strip=True).split()[0]
                if first_p.get_text(strip=True) == "مبلغ تامین شده:":
                    funded_amount = div.find_all("p")[1].get_text(strip=True).split()[0]

        media_tag = element.find("img")

        if media_tag:
            project.project_picture_link = media_tag["src"]

        if needed_fund and funded_amount:
            if needed_fund > funded_amount:
                project.has_opportunity = True
            else:
                project.has_opportunity = False

        warranty_tag = element.find("div", style="margin: 10px 0px; display: flex;")

        if warranty_tag:  #Mechanism could be improved
            warranty_message = warranty_tag.find('p').get_text(strip=True)
            if "تضمین ضمانت نامه تعهد پرداخت برای اصل سرمایه" in warranty_message:
                project.has_warranty = True
            else: 
                project.has_warranty = False

        project.telegram_link = f"https://t.me/smartfunding_project_{idx}"

        project.platform_link = crowdfunding_link

        project.postProjectData(API_BASE_URL, idx)

        print(f"Project Name: {project.project_name}", file=resultFile)
        print(f"Company Title: {project.company_title}", file=resultFile)
        print(f"Estimated Profit: {estimated_profit}", file=resultFile)
        print(f"Media Source: {project.project_picture_link}", file=resultFile)
        print(f"Has Opportunity: {project.has_opportunity}", file=resultFile)
        print(f"Has Warranty: {project.has_warranty}", file=resultFile)

    print("\nExtraction Complete!")

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Usage: python {sys.argv[0]} <html_path> <result_path>")
        sys.exit(1)
    
    html_path = sys.argv[1]
    result_path = sys.argv[2]

    crawler(html_path, result_path)