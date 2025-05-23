from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://zeema.fund/crowdfunding-plan"

platform_data = {
    "name": "zeema",
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

    elements = soup.find_all("div", class_="MuiGrid2-root MuiGrid2-direction-xs-row MuiGrid2-grid-xs-12 MuiGrid2-grid-sm-6 MuiGrid2-grid-md-6 MuiGrid2-grid-lg-4 mui-i2j4vq")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        first_part = element.find("div", class_="MuiCardMedia-root mui-1qvttsi")
        project.project_name = first_part.find_all('span')[0].get_text(strip=True)

        company_title_tag = first_part.find("div", class_="MuiBox-root mui-13jmq0m")
        if company_title_tag:
            project.company_title = company_title_tag.find("img")["alt"]

        profit_tag = element.find("div", class_="MuiBox-root mui-fe7519")
        project.estimated_profit = profit_tag.find_all("span")[0].get_text(strip=True)

        #TODO: The link of the pictures and videos is signed and will be expired after a while
        media_tag = element.find("div", class_="MuiBox-root mui-1jrl3n2").find("img") or element.find("div", class_="MuiBox-root mui-1jrl3n2").find("video")
        if media_tag:
            if media_tag.name == "img":
                project.project_picture_link = "https://zeema.find" + media_tag["src"]
            else:
                project.project_picture_link = media_tag.find("source")["src"]
        
        #TODO: the signed property also makes it too long. I trim it temporarily
        project.project_picture_link = project.project_picture_link[0:255]

        
        funding_tag = element.find("div", class_="MuiBox-root mui-jec8fa")
        percentage = funding_tag.find_all("span")[1].get_text(strip=True)

        if percentage == "100%":
            project.has_opportunity = False
        else:
            project.has_opportunity = True

        warranty_tag = element.find("div", class_="MuiStack-root mui-p5deog")

        if warranty_tag is None:
            project.has_warranty = False
        else:
            project.has_warranty = True

        project.telegram_link = f"https://t.me/zeema_project_{idx}"

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