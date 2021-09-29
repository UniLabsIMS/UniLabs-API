from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_student_url = reverse('student-register')
        cls.all_students_url = reverse('all-students')
        cls.get_student_url_name = 'get-student'
        cls.student_data = {
            'email': cls.fake.email(),
            'department': cls.global_test_department.id,
            'student_id': '1234567X'
        }
        return 

    def tearDown(self):
        return super().tearDown()