from rest_framework.exceptions import ValidationError
from custom_user.permissions import IsAdmin
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import LecturerRegisterSerializer, LecturerReadSerializer, LecturerSummarizedReadSerializer
from rest_framework.permissions import IsAuthenticated
from .models import LabLecturer, Lecturer
from rest_framework.permissions import IsAuthenticated

# Lecturer Register View
class LecturerRegisterAPIView(generics.GenericAPIView):
    serializer_class = LecturerRegisterSerializer
    permission_classes = (IsAuthenticated,IsAdmin) # Only admins may add Lecturers

    def post(self,request): # post request to register new Lecturer
        lecturer = request.data
        serializer = self.serializer_class(data=lecturer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        lecturer_data = serializer.data        
        return Response(lecturer_data,status=status.HTTP_201_CREATED)

# GET request to get all Lecturers in the system as a list
class AllLecturersAPIView(generics.ListAPIView):
    serializer_class=LecturerReadSerializer
    queryset=Lecturer.objects.all()
    permission_classes=(IsAuthenticated,IsAdmin)


# GET request to get all Lecturers of a lab in the system as a list
class LabLecturersAPIView(generics.ListAPIView):
    serializer_class=LecturerSummarizedReadSerializer
    queryset=Lecturer.objects.all()
    permission_classes=(IsAuthenticated,)
    
    def get_queryset(self):
        try:
            lab_lecturers=LabLecturer.objects.filter(lab=self.kwargs.get('lab_id',None)) # get only lab lecturers
            lecturers=[] 
            for lab_lecturer in lab_lecturers:
                lecturers.append(lab_lecturer.lecturer.id)
            return self.queryset.filter(id__in=lecturers)

        except:
            raise ValidationError('Provided lab id invalid')
        