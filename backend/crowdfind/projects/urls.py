from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrowdfundingPlatformViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'platforms', CrowdfundingPlatformViewSet, basename='platform')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]