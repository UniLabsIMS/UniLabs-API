from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_admin_url = reverse('admin-register')
        cls.all_admins_url = reverse('all-admins')
        cls.system_report_url = reverse('system-report')
        cls.admin_data = {
            'email': cls.fake.email()
        }
        return 

    def tearDown(self):
        return super().tearDown()