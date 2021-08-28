from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # POST - New Lab Assistant

    def test_authenticated_admin_can_register_new_lab_assistants(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_lab_assistant_url,self.lab_assistant_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'],self.lab_assistant_data['email'])

    def test_unauthenticated_user_cannot_add_lab_mangers(self):
        res = self.client.post(self.new_lab_assistant_url,self.lab_assistant_data,format="json")
        self.assertEqual(res.status_code, 401)

    def test_authenticated_other_users_cannot_register_new_lab_mangers(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res = self.client.post(self.new_lab_assistant_url,self.lab_assistant_data,format="json")
        self.assertEqual(res.status_code, 403)

    def test_cannot_add_lab_assistant_with_no_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_assistant_data.copy()
        data["email"]=""
        res = self.client.post(self.new_lab_assistant_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lab_assistant_with_invalid_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_assistant_data.copy()
        data["email"]="test"
        res = self.client.post(self.new_lab_assistant_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lab_assistant_with_invalid_lab(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_assistant_data.copy()
        data["lab"]="xx"
        res = self.client.post(self.new_lab_assistant_url,data,format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_add_lab_assistant_with_invalid_department(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_assistant_data.copy()
        data["department"]="xx"
        res = self.client.post(self.new_lab_assistant_url,data,format="json")
        self.assertEqual(res.status_code, 400)