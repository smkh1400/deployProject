from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://isatiscrowd.ir/"

platform_data = {
    "name": "isatis",
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

    elements = soup.find_all("div", class_="flex flex-col items-center bg-white shadow-md rounded-lg w-[400px] min-h-[400px] relative overflow-hidden hover:shadow-2xl cursor-pointer transition-shadow duration-300")

    for idx, element in enumerate(elements, start = 1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        project_name_tag = element.find("h2")
        project.project_name = project_name_tag.text.strip()

        company_tag = element.find("div", class_="p-4 text-center")
        project.company_title = company_tag.find_all('p')[1].get_text(strip=True)

        profit_tag = element.find("div", class_="flex flex-row items-center justify-center w-[60px] relative")
        estimated_profit = ""
        for h1 in profit_tag.find_all('h1'):
            estimated_profit = h1.get_text(strip=True) + estimated_profit
        project.estimated_profit = float(estimated_profit.replace("/", ".")) if estimated_profit is not None else -1

        media_tag = element.find("div", class_="w-full h-[240px] overflow-hidden").find("img") or element.find("div", class_="w-full h-[240px] overflow-hidden").find("video")

        project.project_picture_link = "N/A"

        if media_tag:
            if media_tag.name == "img":
                # print(media_tag.name)
                project.project_picture_link = "https://isatiscrowd.ir" + media_tag["src"]
            else:
                project.project_picture_link = media_tag["src"]


        funding_tag = element.find("div", class_="flex flex-row items-center justify-around w-full mt-4 mb-8")
        h1_elements = funding_tag.find_all("h1", class_="text-gray-500 text-[12px] font-bold")

        project.has_opportunity = False

        if len(h1_elements) != 2:
            project.has_opportunity = False
        elif h1_elements[0].get_text(strip=True) != h1_elements[1].get_text(strip=True):
            project.has_opportunity = True
        else:
            project.has_opportunity = False

        warranty_tag = element.find("div", class_="w-3/4 flex flex-col mb-1 justify-center items-center bg-gradient-to-b from-[#d7ffe8] to-[#c9f2da] border border-green-100 rounded-lg rounded-tr-none text-center mt-2 h-14 overflow-hidden")
        project.has_warranty = False

        if warranty_tag is None:
            project.has_warranty = False
        else:
            project.has_warranty = True

        project.telegram_link = f"https://t.me/isatis_project_{idx}"

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