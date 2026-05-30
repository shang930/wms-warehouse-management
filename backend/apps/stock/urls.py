"""Stock URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.stock.views import MoveStockView, StockMovementViewSet, StockViewSet

app_name = 'stock'
router = DefaultRouter()
router.register(r'', StockViewSet, basename='stock')
router.register(r'movements', StockMovementViewSet, basename='movement')
urlpatterns = [path('move/', MoveStockView.as_view(), name='move_stock'), path('', include(router.urls))]
