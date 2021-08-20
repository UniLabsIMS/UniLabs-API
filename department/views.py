from department.models import Department
from rest_framework import permissions
from custom_user.permissions import IsAdmin
from .serializers import DepartmentReadSerializer,DepartmentWriteSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

#POST request to create department
class DepartmentCreateAPIView(CreateAPIView):
    serializer_class = DepartmentWriteSerializer
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

#GET request to get all departments
class DepartmentListAPIView(ListAPIView):
    serializer_class = DepartmentReadSerializer
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

#GET request to get one department
class DepartmentRetrieveAPIView(RetrieveAPIView):
    serializer_class = DepartmentReadSerializer
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field='id'

#PUT request to edit department
class DepartmentUpdateAPIView(UpdateAPIView):
    serializer_class = DepartmentWriteSerializer
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdmin)
    lookup_field='id'


