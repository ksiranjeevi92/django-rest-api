from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Seialize a token obtain object"""
    @classmethod
    def get_token(cls, user):
        """Create and return a new JWT token"""
        token = super().get_token(user=user)

        #Custom claim added to the JWT payload
        token['username'] = user.name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser

        token['roles'] = list(user.groups.values_list('name', flat=True))

        return token