from rest_framework import permissions
from lab_assistant_user.models import LabAssistant
from custom_user.permissions import IsAdmin
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import LabAssistantReadSerializer, LabAssistantRegisterSerializer
from rest_framework.permissions import IsAuthenticated

# Lab Assistant Register View
class LabAssistantRegisterAPIView(generics.GenericAPIView):
    serializer_class = LabAssistantRegisterSerializer
    permission_classes = (IsAuthenticated,IsAdmin) # Only admins may add lab assistants

    def post(self,request): # post request to register new lab assistant
        lab_assistant = request.data
        serializer = self.serializer_class(data=lab_assistant)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        lab_assistant_data = serializer.data        
        return Response(lab_assistant_data,status=status.HTTP_201_CREATED)

# GET request to get all lab assistants in the system as a list
class AllLabAssistantsAPIView(generics.ListAPIView):
    serializer_class=LabAssistantReadSerializer
    queryset=LabAssistant.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsAdmin)