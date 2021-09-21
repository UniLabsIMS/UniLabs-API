from django.urls import path
from .views import RequestCreateAPIView,RequestListByStudentView,RequestListByLecturerView,RequestsListByLabAPIView,RequestUpdateSerializer

urlpatterns=[
    path('create/',RequestCreateAPIView.as_view(),name='new-request'),
    path('student-requests/',RequestListByStudentView.as_view(),name='student-requests'),
    path('lecturer-requests/',RequestListByLecturerView.as_view(),name='lecturer-requests'),
    path('of-requests/<str:lab_id>', RequestsListByLabAPIView.as_view(), name='requests-of-a-lab'),
    path('approve-or-decline/<str:id>',RequestUpdateSerializer.as_view(),name='approve-or-decline'),


]