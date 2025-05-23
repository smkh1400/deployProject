from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://pulsar.ir/funds"

platform_data = {
    "name": "pulsar",
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

    elements = soup.find_all("div", class_="card mb-4 border-0 overflow-hidden")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        project.project_name = element.find("h4", class_="mt-2 fund-item-title").get_text(strip=True)

        informations = element.find_all("div", class_="d-flex align-items-center")

        #TODO: The company title field in the site was missing for now I put its tarh
        company_tag = informations[1] #TODO: for company title use information[0]
        project.company_title = company_tag.find("strong").get_text(strip=True)

        profit_tag = informations[3]
        project.estimated_profit = profit_tag.find("strong").get_text(strip=True).replace(" %", "")

        project.project_picture_link = "https://pulsar.ir/" + element.find("img", class_="rounded w-100 cur")["src"]

        progress_tag = element.find("div", class_="rounded text-center py-2 bg-primary")
        project.has_opportunity = False if ("تامین مالی شده" in progress_tag.get_text(strip=True)) else True

        warranty_text = informations[4].find("strong").get_text(strip=True)
        project.has_warranty = True if (("تضمین" in warranty_text) or ("ضمانت" in warranty_text)) else False

        project.telegram_link = f"https://t.me/pulsar_project_{idx}"

        project.platform_link = crowdfunding_link

        project.postProjectData(API_BASE_URL, idx)

        print(f"Project Name: {project.project_name}", file=resultFile)
        print(f"Company Title: {project.company_title}", file=resultFile)
        print(f"Estimated Profit: {project.estimated_profit}", file=resultFile)
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