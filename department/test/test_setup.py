from  unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_department_url = reverse('department-create')
        cls.all_departments_url = reverse('all-departments')
        cls.single_department_url_name = 'single-department' # as we need path parameters
        cls.department_data = {
            'name': 'TEST NAME',
            'code': 'TEST CODE',
        }
        return 

    def tearDown(self):
        return super().tearDown()