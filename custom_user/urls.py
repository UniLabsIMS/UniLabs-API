from custom_user.views import UserLoginAPIView
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
]