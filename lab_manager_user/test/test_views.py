from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # POST - New Lab Manager

    def test_authenticated_admin_can_register_new_lab_managers(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_lab_manager_url,self.lab_manager_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'],self.lab_manager_data['email'])

    def test_unauthenticated_user_cannot_add_lab_mangers(self):
        res = self.client.post(self.new_lab_manager_url,self.lab_manager_data,format="json")
        self.assertEqual(res.status_code, 401)

    def test_authenticated_other_users_cannot_register_new_lab_mangers(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.post(self.new_lab_manager_url,self.lab_manager_data,format="json")
        self.assertEqual(res.status_code, 403)

    def test_cannot_add_lab_manager_with_no_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_manager_data.copy()
        data["email"]=""
        res = self.client.post(self.new_lab_manager_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lab_manager_with_invalid_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_manager_data.copy()
        data["email"]="test"
        res = self.client.post(self.new_lab_manager_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lab_manager_with_invalid_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_manager_data.copy()
        data["email"]=self.global_test_lab_manager.email
        res = self.client.post(self.new_lab_manager_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lab_manager_with_invalid_lab(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_manager_data.copy()
        data["lab"]="xx"
        res = self.client.post(self.new_lab_manager_url,data,format="json")
        self.assertEqual(res.status_code, 400)
    
    # GET - all lab managers

    def test_authenticated_admin_users_can_get_a_list_of_lab_managers(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(self.all_lab_managers_url,data_format="json")
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_users_cannot_get_list_of_lab_managers(self):
        res = self.client.get(self.all_lab_managers_url,data_format="json")
        self.assertEqual(res.status_code,401)

    def test_authenticated_non_admin_users_cannot_get_list_of_lab_managers(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.get(self.all_lab_managers_url,data_format="json")
        self.assertEqual(res.status_code,403)