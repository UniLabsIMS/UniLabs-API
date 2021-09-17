from django.urls import path
from .views import LecturerRegisterAPIView, AllLecturersAPIView

urlpatterns = [
    path('register/',LecturerRegisterAPIView.as_view(),name='lecturer-register'),
    path('',AllLecturersAPIView.as_view(),name='all-lecturers'),
]