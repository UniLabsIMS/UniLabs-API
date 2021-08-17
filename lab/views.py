from lab.models import Lab
from rest_framework import permissions
from unilabsAPI.serializers import MultiSerializerAPIView
from custom_user.permissions import IsAdmin
from .serializers import LabReadSerializer,LabWriteSerializer

# end points to CRUD operations on lab
class LabViewSet(MultiSerializerAPIView):
    queryset = Lab.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdmin)
    read_serializer = LabReadSerializer
    write_serializer = LabWriteSerializer
