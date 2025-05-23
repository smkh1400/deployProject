from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://ibcrowd.ir/opportunities/all"

platform_data = {
    "name": "ibcrowd",
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

    elements = soup.find_all("div", class_="col-md-6 col-xl-4 card-deck")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        informations = element.find_all("div", class_="card-text text-start")

        project_tag = informations[0]
        project.project_name = project_tag.find("span").get_text(strip=True)

        company_tag = informations[1]
        project.company_title = company_tag.find("span").get_text(strip=True)

        project.estimated_profit = element.find_all("span", class_="fw-semibold d-block")[1].get_text(strip=True).replace("%", "")

        #TODO: it doesn't have any picture to begin with and I put a `NO IMAGE AVAILABLE`
        project.project_picture_link = "https://demofree.sirv.com/nope-not-here.jpg"

        needed_fund = informations[3].find("span").get_text(strip=True)
        funded_amount = informations[8].find("span").get_text(strip=True)
        project.has_opportunity = False if (needed_fund == funded_amount) else True

        warranty_text = informations[12].get_text(strip=True)
        project.has_warranty = True if (("با تضمین" in warranty_text)) else False

        project.telegram_link = f"https://t.me/ibcrowd_project_{idx}"

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