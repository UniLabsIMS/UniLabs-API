from  unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    def setUp(self):
        super().setUp()
        self.new_department_url = reverse('department-create')
        self.all_departments_url = reverse('all-departments')
        self.single_department_url = reverse('single-department', args=["id"])
        self.department_data = {
            'name': 'TEST NAME',
            'code': 'TEST CODE',
        }
        return 

    def tearDown(self):
        return super().tearDown()