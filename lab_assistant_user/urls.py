from django.urls import path
from .views import LabAssistantRegisterAPIView

urlpatterns = [
    path('register/',LabAssistantRegisterAPIView.as_view(),name='lab-assistant-register'),
]