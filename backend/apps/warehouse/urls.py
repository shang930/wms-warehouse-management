"""Warehouse URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.warehouse.views import BinViewSet, WarehouseViewSet, ZoneViewSet

app_name = 'warehouses'
router = DefaultRouter()
router.register(r'', WarehouseViewSet, basename='warehouse')
router.register(r'zones', ZoneViewSet, basename='zone')
router.register(r'bins', BinViewSet, basename='bin')
urlpatterns = [path('', include(router.urls))]
