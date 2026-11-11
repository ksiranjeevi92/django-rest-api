from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.views import (
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

urlpatterns = [
    # JWT Auth Endpoints
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]