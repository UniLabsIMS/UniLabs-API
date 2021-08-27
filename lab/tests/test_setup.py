from  unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    def setUp(self):
        super().setUp()
        self.new_lab_url = reverse('lab-create')
        self.all_labs_url = reverse('all-labs')
        self.single_lab_url = reverse('single-lab', args=["id"])
        self.lab_data = {
            'name': 'TEST LAB NAME',
            'department': self.test_department.id,
            'location': self.fake.text(),
            'contact_no': '0777568456',
            'contact_email': self.fake.email(),
        }
        return 

    def tearDown(self):
        return super().tearDown()