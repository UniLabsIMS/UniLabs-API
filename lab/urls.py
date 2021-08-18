from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.LabListAPIView.as_view(), name="labs"),
     path('<str:lab_id>', views.LabRetrieveAPIView.as_view(), name="lab"),
     path('create/',views.LabCreateAPIView.as_view(),name="lab-create"),
     path('update/<str:lab_id>',views.LabUpdateAPIView.as_view(),name="lab-update")
]