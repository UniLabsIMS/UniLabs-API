from  unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_lab_url = reverse('lab-create')
        cls.all_labs_url = reverse('all-labs')
        cls.single_lab_url_name = 'single-lab' # as we need path parameters
        cls.labs_of_a_department_url_name = 'labs-of-a-department'
        cls.assign_lec_to_lab_url = reverse('assign-lecturers')
        cls.lab_report_url_name='lab-report'
        cls.lab_data = {
            'name': 'TEST LAB NAME',
            'department': cls.global_test_department.id,
            'location': cls.fake.text(),
            'contact_no': '0777568456',
            'contact_email': cls.fake.email(),
        }
        cls.assign_lecs_to_lab_data={
            'lab': cls.global_test_lab.id,
            'lecturers': [cls.global_test_lecturer_three.id]
        }
        return 

    def tearDown(self):
        return super().tearDown()