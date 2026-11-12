from authentication.permissions import IsAdmin, IsManager
from authentication.serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

REFRESH_COOKIE_PATH = '/api/auth/'

class CustomTokenObtainPairView(TokenObtainPairView):
    """Login endpoint using our custom serializer"""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self,request,*args,**kwargs):
        """Set refresh token in cookie"""
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.pop('refresh', None)

        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,              # HTTPS only (False in local dev)
                samesite='Lax',        # or 'Lax' if frontend is on a different subdomain
                path=REFRESH_COOKIE_PATH,
                max_age=7 * 24 * 60 * 60,
            )
        return response

class CookieTokenRefreshView(TokenRefreshView):
    """Custom refresh token view"""
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh_token')
        if not refresh:
            raise InvalidToken('No refresh token cookie found')

        serializer = self.get_serializer(data={'refresh': refresh})
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.validated_data)  # contains new 'access'

        # If ROTATE_REFRESH_TOKENS=True, a new refresh token is returned; re-set the cookie
        new_refresh = response.data.pop('refresh', None)
        if new_refresh:
            response.set_cookie(
                key='refresh_token', 
                value=new_refresh,
                httponly=True,
                secure=False,
                samesite='Lax',
                path=REFRESH_COOKIE_PATH,
                max_age=7 * 24 * 60 * 60,
            )
        return response
            
class LogoutView(APIView):
    """Logout endpoint: revokes the refresh token and clears the cookie"""
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                ...
        response = Response(status=204)
        response.delete_cookie('refresh_token',
                               samesite='Lax',
                                path=REFRESH_COOKIE_PATH)
        return response
