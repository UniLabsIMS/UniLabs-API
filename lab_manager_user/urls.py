from django.urls import path
from .views import AllLabManagersAPIView, LabManagerRegisterAPIView

urlpatterns = [
    path('register/',LabManagerRegisterAPIView.as_view(),name='lab-manager-register'),
    path('',AllLabManagersAPIView.as_view(),name='all-lab-managers'),
]