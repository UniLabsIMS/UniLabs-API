from department.models import Department
from rest_framework import permissions
from unilabsAPI.serializers import MultiSerializerAPIView
from custom_user.permissions import IsAdmin
from .serializers import DepartmentReadSerializer,DepartmentWriteSerializer

# end points to CRUD operations on department
class DepartmentViewSet(MultiSerializerAPIView):
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdmin)
    read_serializer = DepartmentReadSerializer
    write_serializer = DepartmentWriteSerializer
