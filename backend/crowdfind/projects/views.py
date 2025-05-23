from rest_framework import viewsets
from .models import CrowdfundingPlatform, Project
from .serializers import CrowdfundingPlatformSerializer, ProjectSerializer


class CrowdfundingPlatformViewSet(viewsets.ModelViewSet):
    queryset = CrowdfundingPlatform.objects.all()
    serializer_class = CrowdfundingPlatformSerializer
    lookup_field = 'link'

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer