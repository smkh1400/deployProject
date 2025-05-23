from dataclasses import dataclass
import requests


@dataclass
class ProjectData:
    project_name: str = "N/A"
    company_title: str = "N/A"
    estimated_profit: float = -1
    project_picture_link: str = "N/A"
    has_opportunity: bool = False
    has_warranty: bool = False
    telegram_link: str = "N/A"
    platform_link: str = "N/A"

    def makeProjectData(self):
        project_data = None
        project_data = {
            "project_name": self.project_name,
            "company_title": self.company_title,
            "estimated_profit": self.estimated_profit,
            "project_picture_link": self.project_picture_link,
            "has_opportunity": self.has_opportunity,
            "has_warranty": self.has_warranty,
            "crowdfunding_platform_link": self.platform_link,
            "telegram_link": self.telegram_link
        }
        return project_data
    
    def postProjectData(self, api_base_url, idx):
        project_response = requests.post(f"{api_base_url}/projects/", json=self.makeProjectData())
        if project_response.status_code in [200, 201]:
            print(f"Project {idx} posted.")
        else:
            print(f"Failed to post project {idx}:", project_response.text)