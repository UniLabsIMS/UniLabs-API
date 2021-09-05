from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_lab_assistant_url = reverse('lab-assistant-register')
        cls.lab_assistant_data = {
            'email': cls.fake.email(),
            'lab': cls.global_test_lab.id
        }
        return 

    def tearDown(self):
        return super().tearDown()