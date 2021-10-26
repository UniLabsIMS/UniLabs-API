from lab.models import Lab
from lecturer_user.models import LabLecturer, Lecturer
from custom_user.models import User
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView,GenericAPIView
from rest_framework import permissions, serializers,generics,status
from .serializers import ClearApprovedRequestItemsFromLabForStudentSerailizer, RequestInDepthSerializer, RequestItemReadSerializer, RequestWriteSerializer, StudentCheckForActiveRequestInLabSerializer,UpdateRequestStateSerializer
from .models import Request,RequestItem, RequestState
from custom_user.permissions import IsLabAssistant, IsLabOwner, IsStudent,IsLecturer
from student_user.models import Student
from rest_framework.response import Response
from django.http.response import HttpResponsePermanentRedirect

#view for creation of request
class RequestCreateAPIView(CreateAPIView):
    serializer_class=RequestWriteSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

#get single request
class RequestRetrieveAPIView(RetrieveAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field='id'

#Filter requests by student
class RequestListByStudentView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

    def get_queryset(self):
        try:
            student=Student.objects.get(id=self.request.user.id)
            return self.queryset.filter(student=student,state=RequestState.NEW,)
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


#single endpoints to change request state to approve, decline for lecturers

class RequestUpdateAPIView(GenericAPIView):
    serializer_class = UpdateRequestStateSerializer
    permission_classes = (permissions.IsAuthenticated, IsLecturer)
    queryset = Request.objects.all()
    lookup_field='id'

    def put(self,request, *args, **kwargs):
        req = self.get_object()
        if(req.lecturer.id!=request.user.id):
            return Response({'message':'Unauthorized to approve/decline this request'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data,instance=req)
        if serializer.is_valid():
            serializer.save(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#filter request items by lab and by student
class ApprovedRequestItemsListFromLabForStudentAPIView(ListAPIView):
    serializer_class=RequestItemReadSerializer
    queryset=RequestItem.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabAssistant,IsLabOwner)

    def get_queryset(self):
        try:
            return self.queryset.filter(lab=self.kwargs.get('lab_id',None),student=self.kwargs.get('student_id',None),state=RequestState.APPROVED)
        except:
            raise ValidationError('Provided lab id not valid')

class ClearApprovedRequestItemsFromLabForStudentAPIView(GenericAPIView):
    serializer_class = ClearApprovedRequestItemsFromLabForStudentSerailizer
    permission_classes = (permissions.IsAuthenticated, IsLabAssistant ,IsLabOwner)

    def put(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint for student to check whether he or she has an active request for a lab
class StudentCheckForActiveRequestInLabAPIView(GenericAPIView):
    serializer_class=StudentCheckForActiveRequestInLabSerializer
    permission_classes=(permissions.IsAuthenticated,IsStudent)
    lookup_field='lab_id'

    def get(self,request,*args,**kwargs):
        serializer = self.serializer_class(data={"lab_id":self.kwargs.get('lab_id',None),"student_id":str(request.user.id)})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)