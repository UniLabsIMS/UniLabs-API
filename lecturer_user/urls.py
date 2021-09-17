from django.urls import path
from .views import LecturerRegisterAPIView

urlpatterns = [
    path('register/',LecturerRegisterAPIView.as_view(),name='lecturer-register'),
]