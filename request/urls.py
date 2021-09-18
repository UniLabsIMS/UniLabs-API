from django.urls import path
from .views import RequestCreateAPIView,RequestListApiView

urlpatterns=[
    path('',RequestListApiView.as_view(),name='all-requests'),
    path('create/',RequestCreateAPIView.as_view(),name='new-request'),

]