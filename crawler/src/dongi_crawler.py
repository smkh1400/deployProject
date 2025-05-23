from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://dongi.ir/discover"

platform_data = {
    "name": "dongi",
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

    elements = soup.find_all("div", class_="projectItem col-md-4 col-sm-6 col-xs-12")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        project.project_name = element.find("h3", class_="title-txt").get_text(strip=True)

        company_tag = element.find("div", class_="border-t")
        project.company_title = company_tag.find("span", class_="txt-val").get_text(strip=True)

        project.estimated_profit = element.find("p", class_="text-center txt-bold mar-btm0 profitText").get_text(strip=True).replace("%", "")

        address = element.find("img", class_="image-replacement")["src"]
        if "https://" not in address:
            address = "https://dongi.ir" + address
        project.project_picture_link = address

        progress_tag = element.find("div", class_="col-md-1 col-sm-1 col-xs-1 padd0 d-flex")
        project.has_opportunity = False if ("100%" in progress_tag.get_text(strip=True)) else True

        warranty_tag = element.find("div", style="height: 50px;")
        warranty_text = warranty_tag.find("span").get_text(strip=True)
        project.has_warranty = True if ("با تضمین" in warranty_text) else False

        project.telegram_link = f"https://t.me/dongi_project_{idx}"

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