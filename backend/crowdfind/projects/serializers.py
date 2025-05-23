from rest_framework import serializers
from .models import CrowdfundingPlatform, Project

class CrowdfundingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrowdfundingPlatform
        fields = ['id', 'name', 'link']

class ProjectSerializer(serializers.ModelSerializer):
    crowdfunding_platform = CrowdfundingPlatformSerializer(read_only=True)
    crowdfunding_platform_link = serializers.SlugRelatedField(queryset=CrowdfundingPlatform.objects.all(), slug_field='link', write_only=True, source='crowdfunding_platform')

    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'company_title', 'estimated_profit', 'project_picture_link',
            'has_opportunity', 'has_warranty', 'crowdfunding_platform', 'crowdfunding_platform_link', 'telegram_link'
        ]