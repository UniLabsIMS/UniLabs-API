from django.urls.base import reverse
from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse

class TestSetup(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_request_url=reverse('new-request')
        cls.student_requests_url=reverse('student-requests')
        cls.lecturer_requests_url=reverse('lecturer-requests')
        cls.retrieve_single_request_url_name='get-request'
        cls.requests_of_a_lab_url_name='requests-of-a-lab'
        cls.approve_or_decline_url_name='approve-or-decline'
        cls.approved_request_items_url_name='approved-display-items-in-lab-for-student'
        cls.clear_approved_request_items_url_name='clear-approved-display-items'
        cls.check_student_active_request_url_name = 'check-for-student-active-request-in-lab'
        cls.request_api_view_data = {
            "student": cls.global_test_student.id,
            "lecturer": cls.global_test_lecturer.id,
            "lab": cls.global_test_lab_two.id,
            "reason": "Sample reason 234",
            "display_items_dict": {str(cls.global_test_display_item_four.id): int(cls.global_test_display_item_four.item_count),
            str(cls.global_test_display_item_five.id): int(cls.global_test_display_item_five.item_count)
            }
        }
        return

    def tearDown(self):
        return super().tearDown()
        
