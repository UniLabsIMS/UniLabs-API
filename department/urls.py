from django.urls import path
from . import views
from .views import DepartmentListAPIView,DepartmentRetrieveAPIView,DepartmentCreateAPIView,DepartmentUpdateAPIView

urlpatterns = [
     path('', views.DepartmentListAPIView.as_view(), name="all-departments"),
     path('<str:id>', views.DepartmentRetrieveAPIView.as_view(), name="single-department"),
     path('create/',views.DepartmentCreateAPIView.as_view(),name="department-create"),
     path('update/<str:id>',views.DepartmentUpdateAPIView.as_view(),name="department-update")
]