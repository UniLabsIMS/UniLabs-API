from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ApprovedRequestItemsListFromLabForStudentAPIView, ClearApprovedRequestItemsFromLabForStudentAPIView, RequestCreateAPIView,RequestListByStudentView,RequestListByLecturerView, RequestRetrieveAPIView, RequestUpdateAPIView,RequestsListByLabAPIView,RequestUpdateAPIView, StudentCheckForActiveRequestInLabAPIView


class TestUrls(SimpleTestCase):
    
    def test_new_request_url_and_view(self):
        url = reverse('new-request')
        self.assertEqual(resolve(url).func.view_class, RequestCreateAPIView)
    
    def test_get_request_url_and_view(self):
        url = reverse('get-request',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, RequestRetrieveAPIView)
    
    def test_student_requests_url_and_view(self):
        url = reverse('student-requests')
        self.assertEqual(resolve(url).func.view_class, RequestListByStudentView)
    
    def test_lecturer_requests_url_and_view(self):
        url = reverse('lecturer-requests')
        self.assertEqual(resolve(url).func.view_class, RequestListByLecturerView)
    
    def test_requests_of_a_lab_url_and_view(self):
        url = reverse('requests-of-a-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, RequestsListByLabAPIView)
    
    def test_approve_or_decline_url_and_view(self):
        url = reverse('approve-or-decline',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, RequestUpdateAPIView)
    
    def test_approved_display_items_in_lab_for_student_url_and_view(self):
        url = reverse('approved-display-items-in-lab-for-student',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f','student_id':'539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ApprovedRequestItemsListFromLabForStudentAPIView)
    
    def test_clear_approved_display_items_url_and_view(self):
        url = reverse('clear-approved-display-items')
        self.assertEqual(resolve(url).func.view_class, ClearApprovedRequestItemsFromLabForStudentAPIView)

    def test_check_for_student_active_request_in_lab_url_and_view(self):
        url = reverse('check-for-student-active-request-in-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, StudentCheckForActiveRequestInLabAPIView)
    

    