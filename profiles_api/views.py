from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):
    """Test API View"""

    serializers_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP method as fucntion (get , post, patch , put , delete)',
            'Is similar to a tradition Django view',
            "Gives you the most control over your application",
            "Is mapped mannual to URLs"
        ]

        return Response(
            {
                'message': 'Hello',
                'an_apiview': an_apiview
            }
        )

    def post(self,request):
        """Create a hello messgae with our name"""
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                "message": message
            })
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )

    def put(self, request, pk=None):
        """Handle updating of an object"""
        return Response({'method': 'PUT'})

    def pathch(self,request,pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses action (list, create, retreive, update , partial_update)',
            'Automatically mapt to URLS using Routers',
            'Providers more functionality with less code'
        ]

        return Response({'message': "Hello", 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if  serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                "message": message
            })
        else:
            return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle gettina an object by it's ID"""
        return Response(
            {
                'http_method': "GET"
            }
        )

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response(
            {
                "http_method": "PUT"
            }
        )


    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response(
            {
                'http_method': "Patch"
            }
        )
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({"http_method": "DELETE"})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles."""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

