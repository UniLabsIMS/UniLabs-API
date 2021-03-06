from django.urls import path
from .views import ApprovedRequestItemsListFromLabForStudentAPIView, ClearApprovedRequestItemsFromLabForStudentAPIView, RequestCreateAPIView,RequestListByStudentView,RequestListByLecturerView, RequestRetrieveAPIView,RequestsListByLabAPIView,RequestUpdateAPIView, StudentCheckForActiveRequestInLabAPIView

urlpatterns=[
    path('create/',RequestCreateAPIView.as_view(),name='new-request'),
    path('<str:id>',RequestRetrieveAPIView.as_view(),name='get-request'),
    path('student-requests/',RequestListByStudentView.as_view(),name='student-requests'),
    path('lecturer-requests/',RequestListByLecturerView.as_view(),name='lecturer-requests'),
    path('of-requests/<str:lab_id>', RequestsListByLabAPIView.as_view(), name='requests-of-a-lab'),
    path('approve-or-decline/<str:id>',RequestUpdateAPIView.as_view(),name='approve-or-decline'),
    path('approved-request-items/<str:lab_id>/<str:student_id>', ApprovedRequestItemsListFromLabForStudentAPIView.as_view(), name='approved-display-items-in-lab-for-student'),
    path('clear-approved-request-items/', ClearApprovedRequestItemsFromLabForStudentAPIView.as_view(), name='clear-approved-display-items'), 
    path('check-student-active-request/<str:lab_id>', StudentCheckForActiveRequestInLabAPIView.as_view(), name='check-for-student-active-request-in-lab'), 
]