from django.urls import path
from .views import LabManagerRegisterAPIView

urlpatterns = [
    path('register/',LabManagerRegisterAPIView.as_view(),name='lab-manager-register'),
]