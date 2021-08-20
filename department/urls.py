from django.urls import path,include
from . import views
from .views import DepartmentListAPIView,DepartmentRetrieveAPIView,DepartmentCreateAPIView,DepartmentUpdateAPIView

urlpatterns = [
     path('', views.DepartmentListAPIView.as_view(), name="departments"),
     path('<str:id>', views.DepartmentRetrieveAPIView.as_view(), name="department"),
     path('create/',views.DepartmentCreateAPIView.as_view(),name="department-create"),
     path('update/<str:id>',views.DepartmentUpdateAPIView.as_view(),name="department-update")
]