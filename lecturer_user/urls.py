from django.urls import path
from .views import LabLecturersAPIView, LecturerRegisterAPIView, AllLecturersAPIView

urlpatterns = [
    path('register/',LecturerRegisterAPIView.as_view(),name='lecturer-register'),
    path('of-lab/<str:lab_id>',LabLecturersAPIView.as_view(),name='lecturers-of-lab'),
    path('',AllLecturersAPIView.as_view(),name='all-lecturers'),
]