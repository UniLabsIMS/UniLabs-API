from django.urls import path
from .views import RequestCreateAPIView

urlpatterns=[
    path('create/',RequestCreateAPIView.as_view(),name='new-request'),
]