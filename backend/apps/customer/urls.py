"""Customer URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.customer.views import CustomerViewSet

app_name = 'customers'
router = DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')
urlpatterns = [path('', include(router.urls))]
