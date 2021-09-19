from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework import permissions, serializers
from .serializers import RequestInDepthSerializer, RequestWriteSerializer
from .models import Request
from custom_user.permissions import IsStudent,IsLecturer

#view for creation of request
class RequestCreateAPIView(CreateAPIView):
    serializer_class=RequestWriteSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsStudent)

#view all request date
class RequestListApiView(ListAPIView):
    serializer_class=RequestInDepthSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    # def get_queryset(self,request):
    #     try:
    #         s = Student.objects.get(id=request.user.id)
    #         return self.queryset.filter(student = s) 
    #     except:
    #         raise ValidationError("Invalid ID")

# add seperate end points to get requests filter by  lecturer,student, lab

# add a single endpoints to change request state to approve, decline for lecturers