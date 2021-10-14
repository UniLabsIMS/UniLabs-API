from django.db import transaction
from rest_framework.response import Response
from lecturer_user.models import LabLecturer
from rest_framework.generics import CreateAPIView, GenericAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView
from lab.models import Lab
from rest_framework import permissions, status
from custom_user.permissions import IsAdmin
from .serializers import LabAssignLecturerSerializer, LabInDepthReadSerializer, LabReportReadSerializer, LabUpdateSerializer,LabWriteSerializer
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
            raise ValidationError('Provided department id not valid')


class LabAssignLecturerAPIView(GenericAPIView):
    serializer_class = LabAssignLecturerSerializer
    permission_classes = (permissions.IsAuthenticated,IsAdmin)

    @transaction.atomic
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LabReportAPIView(GenericAPIView):
    serializer_class =LabReportReadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field='lab_id'

    def get(self,request,*args,**kwargs):
        serializer = self.serializer_class(data={'lab_id':self.kwargs.get('lab_id',None)})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        