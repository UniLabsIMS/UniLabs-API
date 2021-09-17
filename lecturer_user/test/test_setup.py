from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_lecturer_url = reverse('lecturer-register')
        cls.all_lecturers_url = reverse('all-lecturers')
        cls.lecturer_data = {
            'email': cls.fake.email(),
            'department': cls.global_test_department.id,
            'lecturer_id': '123456787X',
            'permitted_labs':[cls.global_test_lab.id, cls.global_test_lab_two.id]
        }
        return 

    def tearDown(self):
        return super().tearDown()