from  unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_lab_url = reverse('lab-create')
        cls.all_labs_url = reverse('all-labs')
        cls.single_lab_url = 'single-lab' # as we need path parameters
        cls.lab_data = {
            'name': 'TEST LAB NAME',
            'department': cls.global_test_department.id,
            'location': cls.fake.text(),
            'contact_no': '0777568456',
            'contact_email': cls.fake.email(),
        }
        return 

    def tearDown(self):
        return super().tearDown()