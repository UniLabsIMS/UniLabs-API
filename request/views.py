from lab.models import Lab
from lecturer_user.models import LabLecturer, Lecturer
from custom_user.models import User
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView,GenericAPIView
from rest_framework import permissions, serializers,generics,status
from .serializers import RequestInDepthSerializer, RequestItemReadSerializer, RequestWriteSerializer,UpdateRequestStateSerializer
from .models import Request,RequestItem, RequestState
from custom_user.permissions import IsStudent,IsLecturer
from student_user.models import Student
from rest_framework.response import Response
from django.http.response import HttpResponsePermanentRedirect

#view for creation of request
class RequestCreateAPIView(CreateAPIView):
    serializer_class=RequestWriteSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

#Filter requests by student
class RequestListByStudentView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

    def get_queryset(self):
        try:
            student=Student.objects.get(id=self.request.user.id)
            return self.queryset.filter(student=student,state=RequestState.NEW)
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
            return self.queryset.filter(lecturer=lecturer,state=RequestState.NEW)
        except:
            raise ValidationError("Invalid ID")

#filter requests by lab
class RequestsListByLabAPIView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(lab=self.kwargs.get('lab_id',None)) # get only items for the passed id in url
        except:
            raise ValidationError('Provided lab id not valid')


# add a single endpoints to change request state to approve, decline for lecturers

class RequestUpdateSerializer(GenericAPIView):
    serializer_class = UpdateRequestStateSerializer
    permission_classes = (permissions.IsAuthenticated, IsLecturer)
    queryset = Request.objects.all()
    lookup_field='id'

    def put(self,request, *args, **kwargs):
        req = self.get_object()
        # import pdb;pdb.set_trace()
        serializer = self.get_serializer(data=request.data,instance=req)
        if serializer.is_valid():
            serializer.save(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # valdiate method what you have check
    # 1. the data.get('state')==RequestState.APPROVED || data.get('state')==RequestState.DICLINED
    # 2. check whther the request instane passed has state new

    # def save(self,request):
    #     request = self.instance
    #     request.state=data.get('state')
    #     request.save()
    #     request_items = ReItn.objectrs.filter(request=request)
    #     for req_item in request items:
    #         req_item.state = data.get('state') 
    #         req.save()
    #     return