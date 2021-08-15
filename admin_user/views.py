from custom_user.permissions import IsAdmin
from custom_user.models import User
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AdminRegisterSerializer
from rest_framework.permissions import IsAuthenticated

# Admin Register View
class AdminRegisterView(generics.GenericAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = (IsAuthenticated,IsAdmin) # Only admins may add other admins

    def post(self,request): # post request to register admin
        admin = request.data
        serializer = self.serializer_class(data=admin)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        admin_data = serializer.data        
        return Response(admin_data,status=status.HTTP_201_CREATED)


class InitialSystemAdminRegiterView(generics.GenericAPIView):
    serializer_class = AdminRegisterSerializer

    def post(self,request): # post request to register admin

        if(User.objects.all().count() != 0):
            return Response({'error': 'system already has at least one admin'},status=status.HTTP_400_BAD_REQUEST)
        admin = request.data
        serializer = self.serializer_class(data=admin)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        admin_data = serializer.data        
        return Response(admin_data,status=status.HTTP_201_CREATED)
