from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
from lab.models import Lab
from rest_framework import permissions
from custom_user.permissions import IsAdmin
from .serializers import LabInDepthReadSerializer, LabUpdateSerializer,LabWriteSerializer
from rest_framework.exceptions import ValidationError

#POST request to create lab
class LabCreateAPIView(CreateAPIView):
    serializer_class = LabWriteSerializer
    queryset = Lab.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

#GET request to get all labs
class LabListAPIView(ListAPIView):
    serializer_class = LabInDepthReadSerializer
    queryset = Lab.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

#GET request to get one lab
class LabRetrieveAPIView(RetrieveAPIView):
    serializer_class = LabInDepthReadSerializer
    queryset = Lab.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field='id'

#PUT request to edit lab
class LabUpdateAPIView(UpdateAPIView):
    serializer_class = LabUpdateSerializer
    queryset = Lab.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsAdmin)
    lookup_field='id'

#GET request to get labs of a specific department
class LabListByDepartmentAPIView(ListAPIView):
    serializer_class=LabInDepthReadSerializer
    queryset=Lab.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(department=self.kwargs.get('department_id',None)) # get only lab for the passed id in url
        except:
            raise ValidationError('Provided Lab id not valid')
