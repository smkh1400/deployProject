from django.db import models

class CrowdfundingPlatform(models.Model):
    name = models.CharField(max_length=255, null=False)
    link = models.URLField(max_length=255, null=False, unique=True)

    def __str__(self):
        return f"{self.name=}, {self.link=}"

class Project(models.Model):
    project_name = models.CharField(max_length=255, null=False)
    company_title = models.CharField(max_length=255, null=False)
    estimated_profit = models.FloatField(null=False)
    project_picture_link = models.URLField(max_length=255, null=False)
    has_opportunity = models.BooleanField(null=False, default=True)
    has_warranty = models.BooleanField(null=False, default=True)
    crowdfunding_platform = models.ForeignKey(CrowdfundingPlatform, on_delete=models.CASCADE, null=False, to_field='link')
    telegram_link = models.URLField(max_length=255, null=False, unique=True, default="")

    def __str__(self):
        return f"{self.project_name=}, {self.company_title=}, {self.estimated_profit=}, {self.project_picture_link=}, {self.has_opportunity=}, {self.crowdfunding_platform=}, {self.telegram_link=}"

