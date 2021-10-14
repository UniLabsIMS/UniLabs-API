from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.LabListAPIView.as_view(), name="all-labs"),
     path('<str:id>', views.LabRetrieveAPIView.as_view(), name="single-lab"),
     path('create/',views.LabCreateAPIView.as_view(),name="lab-create"),
     path('update/<str:id>',views.LabUpdateAPIView.as_view(),name="lab-update"),
     path('of-department/<str:department_id>', views.LabListByDepartmentAPIView.as_view(), name='labs-of-a-department'),
     path('assign-lecturers/', views.LabAssignLecturerAPIView.as_view(), name='assign-lecturers'),
     path('lab-report/<str:lab_id>',views.LabReportAPIView.as_view(), name='lab-report'),
]