"""Capital URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.capital.views import AssetViewSet, PalletViewSet
app_name = 'capital'
router = DefaultRouter(); router.register(r'', AssetViewSet, basename='asset'); router.register(r'pallets', PalletViewSet, basename='pallet')
urlpatterns = [path('', include(router.urls))]
