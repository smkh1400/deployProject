from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://cfrazavi.ir/"

platform_data = {
    "name": "razavi",
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

    elements = soup.find_all("div", class_="col-12 col-md-6 col-xl-6")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        project.project_name = element.find('h4', style="padding: 8px; font-size: 12px").get_text(strip=True)

        informations = element.find_all("div", class_="project-features-row col-12")
        
        company_title_tag = informations[1]
        project.company_title = company_title_tag.find("p", class_="col-6").get_text(strip=True)

        profit_tag = informations[6]
        project.estimated_profit = profit_tag.find("p", class_="col-6").get_text(strip=True).replace(" درصد", "")

        media_tag = element.find("div", class_="card").find("img")
        project.project_picture_link = "https://cfrazavi.ir" + media_tag["src"]
        
        progress_text = element.find("div", class_="progress-bar progress-bar-striped progress-bar-animated bg-success").get_text(strip=True)
        project.has_opportunity = False if (("100" in progress_text)) else True

        warranty_tag = informations[8]
        warranty_text = warranty_tag.find("p", class_="col-12").get_text(strip=True)

        project.has_warranty = True if (("ضمانت" in warranty_text) or ("تضمین" in warranty_text)) else False

        project.telegram_link = f"https://t.me/razavi_project_{idx}"

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