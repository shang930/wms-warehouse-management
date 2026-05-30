"""DN URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.dn.views import DNViewSet

app_name = 'dn'
router = DefaultRouter()
router.register(r'', DNViewSet, basename='dn')
urlpatterns = [path('', include(router.urls))]
