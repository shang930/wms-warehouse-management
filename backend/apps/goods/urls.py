"""Goods URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.goods.views import GoodsBrandViewSet, GoodsCategoryViewSet, GoodsUnitViewSet, GoodsViewSet

app_name = 'goods'
router = DefaultRouter()
router.register(r'categories', GoodsCategoryViewSet, basename='category')
router.register(r'units', GoodsUnitViewSet, basename='unit')
router.register(r'brands', GoodsBrandViewSet, basename='brand')
router.register(r'', GoodsViewSet, basename='goods')
urlpatterns = [path('', include(router.urls))]
