from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



urlpatterns = [
    path("signup/", views.UserCreationView.as_view(), name="signup"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('profile-detail/<int:id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('list-location/', views.ListLocationUsers.as_view(), name='list-location'),
    path('list-users/', views.ListAllUsers.as_view(), name='list-users')

]