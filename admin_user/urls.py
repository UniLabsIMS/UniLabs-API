from django.urls import path
from .views import AdminRegisterAPIView,InitialSystemAdminRegiterAPIView

urlpatterns = [
    path('register/',AdminRegisterAPIView.as_view(),name='admin-register'),
    path('register/first/',InitialSystemAdminRegiterAPIView.as_view(),name='init-admin-register'), # to add first admin to the system
]