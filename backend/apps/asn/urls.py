"""ASN URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.asn.views import ASNViewSet

app_name = 'asn'
router = DefaultRouter()
router.register(r'', ASNViewSet, basename='asn')
urlpatterns = [path('', include(router.urls))]
