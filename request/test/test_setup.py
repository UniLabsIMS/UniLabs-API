from django.urls.base import reverse
from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse

class TestSetup(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_request_url=reverse('new-request')
        cls.all_requests_url=reverse('all-requests')
        cls.request_api_view_data = {
            "student": cls.global_test_request_one.student.id,
            "lecturer": cls.global_test_request_one.lecturer.id,
            "reason": "Sample reason 234",
            "display_items_dict": {str(cls.global_test_request_item_one.display_item.id): int(cls.global_test_request_item_one.quentity)}
        }
        return

    def tearDown(self):
        return super().tearDown()
        
