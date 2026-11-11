from authentication.permissions import IsAdmin, IsManager
from authentication.serializers import CustomTokenObtainPairSerializer

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Login endpoint using our custom serializer"""
    serializer_class = CustomTokenObtainPairSerializer