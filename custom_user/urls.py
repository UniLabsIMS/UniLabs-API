from django.urls import path
from admin_user.views import AdminRegisterView,InitialSystemAdminRegiterView

urlpatterns = [
    path('register/',AdminRegisterView.as_view(),name='admin-register'),
    path('register/first/',InitialSystemAdminRegiterView.as_view(),name='init-admin-register'), # to add first admin to the system
]