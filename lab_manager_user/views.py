from custom_user.permissions import IsAdmin
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import LabManagerRegisterSerializer
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

