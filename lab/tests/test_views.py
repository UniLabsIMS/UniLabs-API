from .test_setup import TestSetUp

class TestViews(TestSetUp):
    #post - new lab
    def test_authenticated_admin_can_create_labs(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_lab_url,self.lab_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone('id')
    
    def test_authenticated_other_users_cannot_create_department(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_lab_url,self.lab_data,format="json")
        self.assertEqual(res.status_code,403)
    
    def test_cannot_create_lab_without_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data=self.lab_data.copy()
        data['name']=""
        res=self.client.post(self.new_lab_url,data,format='json')
        self.assertEqual(res.status_code,400)

    def test_cannot_create_lab_with_duplicate_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data=self.lab_data.copy()
        data['name']=self.global_test_lab.name
        res=self.client.post(self.new_lab_url,data,format='json')
        self.assertEqual(res.status_code,400)

    def test_lab_creation_must_fail_if_department_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_data.copy()
        data['department'] = '123' # Invalid department id
        res = self.client.post(self.new_lab_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_lab_without_department(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data=self.lab_data.copy()
        data['department']=""
        res=self.client.post(self.new_lab_url,data,format="json")
        self.assertEqual(res.status_code,400)


    
