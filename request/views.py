from lab.models import Lab
from lecturer_user.models import LabLecturer, Lecturer
from custom_user.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView,GenericAPIView
from rest_framework import permissions, serializers,generics,status
from .serializers import RequestInDepthSerializer, RequestItemReadSerializer, RequestWriteSerializer
from .models import Request,RequestItem
from custom_user.permissions import IsStudent,IsLecturer
from student_user.models import Student
from rest_framework.response import Response
from django.http.response import HttpResponsePermanentRedirect

#view for creation of request
class RequestCreateAPIView(CreateAPIView):
    serializer_class=RequestWriteSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

#view all request date
# class RequestListApiView(ListAPIView):
#     serializer_class=RequestInDepthSerializer
#     queryset=Request.objects.all()
#     permission_classes=(permissions.IsAuthenticated,)

    # def get_queryset(self,request):
    #     try:
    #         s = Student.objects.get(id=request.user.id)
    #         return self.queryset.filter(student = s) 
    #     except:
    #         raise ValidationError("Invalid ID")

# add seperate end points to get requests filter by  lecturer,student, lab

#Filter requests by student
class RequestListByStudentView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

    def get_queryset(self):
        try:
            student=Student.objects.get(id=self.request.user.id)
            return self.queryset.filter(student=student)
        except:
            raise ValidationError("Invalid ID")

#filter requests by lecturer
class RequestListByLecturerView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLecturer)

    def get_queryset(self):
        try:
            lecturer=Lecturer.objects.get(id=self.request.user.id)
            return self.queryset.filter(lecturer=lecturer)
        except:
            raise ValidationError("Invalid ID")

#filter requests by lab
class RequestsListByLabAPIView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLecturer)

    def get_queryset(self):
        try:
            return self.queryset.filter(lab=self.kwargs.get('lab_id',None)) # get only items for the passed id in url
        except:
            raise ValidationError('Provided lab id not valid')


        

# add a single endpoints to change request state to approve, decline for lecturers