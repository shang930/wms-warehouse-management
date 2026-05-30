"""CycleCount URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.cyclecount.views import CycleCountViewSet
app_name = 'cyclecount'
router = DefaultRouter(); router.register(r'', CycleCountViewSet, basename='cyclecount')
urlpatterns = [path('', include(router.urls))]
