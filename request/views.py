from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework import permissions
from .serializers import RequestWriteSerializer
from .models import Request

class RequestCreateAPIView(CreateAPIView):
    serializer_class=RequestWriteSerializer
    queryset=Request.objects.all()
    permission_classes=(permissions.IsAuthenticated,)