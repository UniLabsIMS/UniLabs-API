from rest_framework import permissions
from lab_manager_user.models import LabManager
from custom_user.permissions import IsAdmin
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import LabManagerReadSerializer, LabManagerRegisterSerializer
from rest_framework.permissions import IsAuthenticated

# Lab Manager Register View
class LabManagerRegisterAPIView(generics.GenericAPIView):
    serializer_class = LabManagerRegisterSerializer
    permission_classes = (IsAuthenticated,IsAdmin) # Only admins may add lab managers

    def post(self,request): # post request to register new lab manager
        lab_manager = request.data
        serializer = self.serializer_class(data=lab_manager)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        lab_manager_data = serializer.data        
        return Response(lab_manager_data,status=status.HTTP_201_CREATED)

# GET request to get all lab managers in the system as a list
class AllLabManagersAPIView(generics.ListAPIView):
    serializer_class=LabManagerReadSerializer
    queryset=LabManager.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsAdmin)