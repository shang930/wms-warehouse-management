"""User management URLs."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.users import views

app_name = 'users'
router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'menus', views.MenuViewSet, basename='menu')
urlpatterns = [
    path('logs/', views.OperationLogListView.as_view(), name='operation_logs'),
    path('', include(router.urls)),
]
