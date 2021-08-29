from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # Login Tests

    def test_admin_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.admin_login_data,format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.admin_login_data['email'])
        self.assertIsNotNone(res.data['token'])

    def test_lab_manager_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.lab_manager_login_data,format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.lab_manager_login_data['email'])
        self.assertIsNotNone(res.data['other_details']['lab']['id'])
        self.assertIsNotNone(res.data['token'])

    def test_lab_assistant_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.lab_assistant_login_data,format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.lab_assistant_login_data['email'])
        self.assertIsNotNone(res.data['other_details']['lab']['id'])
        self.assertIsNotNone(res.data['token'])

    def test_cannot_login_using_invalid_email(self):
        data = self.admin_login_data.copy()
        data['email'] ="error@gmail.com"
        res = self.client.post(self.login_url,data,format="json")
        self.assertEqual(res.status_code, 401)
    
    def test_cannot_login_using_invalid_password(self):
        data = self.admin_login_data.copy()
        data['password'] ="pass"
        res = self.client.post(self.login_url,data,format="json")
        self.assertEqual(res.status_code, 401)