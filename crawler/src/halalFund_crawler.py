from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys
from urllib.parse import quote

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://halalfund.ir/"

platform_data = {
    "name": "halalfund",
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

    elements = soup.find_all("div", class_="ant-col ProjectItemWrapper ant-col-xs-24 ant-col-sm-12 ant-col-md-12 ant-col-lg-8 ant-col-xl-8")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        project_name_tag = element.find("div", class_="projectItemTitleWrapper")
        project.project_name = project_name_tag.find_all('span')[0].get_text(strip=True)

        info_tag = element.find("div", style="margin: 20px 10px;").find_all("p")
        project.company_title = info_tag[1].get_text(strip=True).replace("متقاضی: ", "")

        if len(info_tag) > 4:
            project.estimated_profit = info_tag[3].get_text(strip=True).split(" ")[-1].replace("%", "")

        media_tag = element.find("div", class_="projectItemImage").find("img")

        if media_tag:
            project.project_picture_link = quote(media_tag["src"], safe=":/?#=&")

        percentage = element.find("div", class_="projectItemSliderCircle").get_text(strip=True)
        if percentage == "100%":
            project.has_opportunity = False
        else:
            project.has_opportunity = True

        if len(info_tag) > 4:
            warranty_message = info_tag[4].get_text(strip=True)
        else:
            warranty_message = info_tag[3].get_text(strip=True)

        if "با تضمین" in warranty_message:
            project.has_warranty = True
        else:
            project.has_warranty = False

        project.telegram_link = f"https://t.me/halalfund_project_{idx}"

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