from django.urls import path
from .views import AdminRegisterAPIView, AllAdminsAPIView,InitialSystemAdminRegiterAPIView, SystemReportAPIView

urlpatterns = [
    path('register/',AdminRegisterAPIView.as_view(),name='admin-register'),
    path('register/first/',InitialSystemAdminRegiterAPIView.as_view(),name='init-admin-register'), # to add first admin to the system
    path('system-report/',SystemReportAPIView.as_view(),name='system-report'), # to get system report
    path('',AllAdminsAPIView.as_view(),name='all-admins'),
]