from django.urls import path
from .views import AllStudentsAPIView, StudentRegisterAPIView

urlpatterns = [
    path('register/',StudentRegisterAPIView.as_view(),name='student-register'),
    path('',AllStudentsAPIView.as_view(),name='all-students'),
]