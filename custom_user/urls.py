from custom_user.views import ChangePasswordAPIView, RefreshUserAuthAPIView, UpdateProfileDetialsAPIView, UserLoginAPIView
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('change-password/',ChangePasswordAPIView.as_view(), name='change-password'),
    path('update-profile/',UpdateProfileDetialsAPIView.as_view(), name='update-profile'),
    path('refresh-auth/',RefreshUserAuthAPIView.as_view(), name='refresh-auth'),
]