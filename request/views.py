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
    permission_classes=(permissions.IsAuthenticated,IsLecturer)