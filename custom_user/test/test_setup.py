from custom_user.utils.default_passwords import DefaultPasswords
from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse



class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.login_url = reverse('login')
        cls.admin_login_data={
            'email':cls.global_test_admin.email,
            'password':DefaultPasswords.DEFAULT_DEBUG_ADMIN_PASSWORD, # default password used while regestering new user in debug mode
        }
        cls.lab_manager_login_data={
            'email':cls.global_test_lab_manager.email,
            'password':DefaultPasswords.DEFAULT_DEBUG_LAB_MANAGER_PASSWORD, # default password used while regestering new lab manager user in debug mode
        }
        cls.lab_assistant_login_data={
            'email':cls.global_test_lab_assistant.email,
            'password':DefaultPasswords.DEFAULT_DEBUG_LAB_ASSISTANT_PASSWORD, # default password used while regestering new lab assistant user in debug mode
        }
        return 

    def tearDown(self):
        return super().tearDown()