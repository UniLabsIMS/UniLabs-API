from django.urls import path
from .views import AllStudentsAPIView, SingleStudentAPIView, StudentRegisterAPIView

urlpatterns = [
    path('register/',StudentRegisterAPIView.as_view(),name='student-register'),
    path('',AllStudentsAPIView.as_view(),name='all-students'),
    path('<str:student_id>',SingleStudentAPIView.as_view(),name='get-student'),
]