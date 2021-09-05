from django.urls import path
from .views import AllLabAssistantsAPIView, LabAssistantRegisterAPIView

urlpatterns = [
    path('register/',LabAssistantRegisterAPIView.as_view(),name='lab-assistant-register'),
    path('',AllLabAssistantsAPIView.as_view(),name='all-lab-assistants'),
]