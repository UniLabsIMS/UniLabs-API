
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # GET - departments 

    def test_unauthenticated_user_cannot_get_departments(self):
        res = self.client.get(self.all_departments_url,format='json')
        self.assertEqual(res.status_code, 401)

    def test_authnaticated_user_can_get_departments(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(self.all_departments_url,format='json')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data),0)

    # POST - new department
    def test_authenticated_admin_can_create_departments(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_department_url,self.department_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone('id')

    def test_authenticated_other_users_cannot_create_departments(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.post(self.new_department_url,self.department_data,format="json")
        self.assertEqual(res.status_code, 403)

    def test_cannot_create_department_with_no_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['name']=""
        res = self.client.post(self.new_department_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_department_with_no_code(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['code']=""
        res = self.client.post(self.new_department_url,data,format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_create_department_with_duplicate_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['name']=self.global_test_department.name # this department name is already used in global test setup
        res = self.client.post(self.new_department_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_department_with_duplicate_code(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['code']=self.global_test_department.code  # this department code is already is used in global test setup
        res = self.client.post(self.new_department_url,data,format="json")
        self.assertEqual(res.status_code, 400)