from bs4 import BeautifulSoup
import requests
from data import ProjectData
import sys

API_BASE_URL = "http://localhost:8000/api"

crowdfunding_link = "https://www.investorun.com/companies"

platform_data = {
    "name": "investorun",
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

    elements = soup.find_all("a", class_="lg:max-w-[522px] max-w-full transition-transform ease-in-out duration-300 hover:scale-95 hover:duration-500 relative w-full")

    for idx, element in enumerate(elements, start=1):
        print(f"\n**Project {idx}:**", file=resultFile)

        project = ProjectData()

        #TODO: the name of the project was the same as the name of the company and there was no information about the name of the project
        project.project_name = element.find("h3", class_="text-4xl font-bold text-natural_primary_900 text-start flex h-full items-end pt-2").get_text(strip=True)

        project.company_title = element.find("p", class_="font-semibold text-natural_primary_900 text-sm truncate max-w-[90%] pl-2").get_text(strip=True)
        # informations = element.find_all("div", class_="d-flex align-items-center")

        #TODO: it can't find the estimated profit with full class description but inline-block is sufficient but risky
        project.estimated_profit = element.find("div", class_="inline-block").get_text(strip=True).replace(" درصد", "")

        project.project_picture_link = element.find("div", class_="rounded-t-32").find("img")["src"]

        progress_tag = element.find("div", class_="flex items-center gap-1").find("span")
        project.has_opportunity = False if ("100" in progress_tag.get_text(strip=True)) else True

        warranty_text = element.find_all("span", class_="block font-bold text-base xl:text-base text-xs text-right")[1].get_text(strip=True)
        project.has_warranty = False if (("بدون" in warranty_text)) else True

        project.telegram_link = f"https://t.me/investorun_project_{idx}"

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