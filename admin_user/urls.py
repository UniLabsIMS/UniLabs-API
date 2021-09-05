from django.urls import path
from .views import AdminRegisterAPIView, AllAdminsAPIView,InitialSystemAdminRegiterAPIView

urlpatterns = [
    path('register/',AdminRegisterAPIView.as_view(),name='admin-register'),
    path('register/first/',InitialSystemAdminRegiterAPIView.as_view(),name='init-admin-register'), # to add first admin to the system
    path('',AllAdminsAPIView.as_view(),name='all-admins'),
]