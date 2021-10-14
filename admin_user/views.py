from rest_framework import permissions
from admin_user.models import Admin
from custom_user.permissions import IsAdmin
from custom_user.models import User
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import AdminReadSerializer, AdminRegisterSerializer, SystemReportReadSerializer
from rest_framework.permissions import IsAuthenticated

# Admin Register View
class AdminRegisterAPIView(generics.GenericAPIView):
    serializer_class = AdminRegisterSerializer
    permission_classes = (IsAuthenticated,IsAdmin) # Only admins may add other admins

    def post(self,request): # post request to register admin
        admin = request.data
        serializer = self.serializer_class(data=admin)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        admin_data = serializer.data        
        return Response(admin_data,status=status.HTTP_201_CREATED)


class InitialSystemAdminRegiterAPIView(generics.GenericAPIView):
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

# GET request to get all admins in the system as a list
class AllAdminsAPIView(generics.ListAPIView):
    serializer_class=AdminReadSerializer
    queryset=Admin.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsAdmin)

#GET system report
class SystemReportAPIView(generics.GenericAPIView):
    serializer_class =SystemReportReadSerializer
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    def get(self,request,*args,**kwargs):
        serializer = self.serializer_class(data={})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)