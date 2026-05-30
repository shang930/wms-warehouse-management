"""Authentication URLs."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.CurrentUserView.as_view(), name='current_user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
