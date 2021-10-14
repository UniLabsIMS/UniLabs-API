
from .test_setup import TestSetUp
from django.urls import reverse
class TestViews(TestSetUp):
    # POST - new department
    def test_authenticated_admin_can_create_departments(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_department_url,self.department_data,format="multipart")
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone('id')

    def test_authenticated_other_users_cannot_create_departments(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.post(self.new_department_url,self.department_data,format="multipart")
        self.assertEqual(res.status_code, 403)

    def test_cannot_create_department_with_no_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['name']=""
        res = self.client.post(self.new_department_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_department_with_no_code(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['code']=""
        res = self.client.post(self.new_department_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_create_department_with_duplicate_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['name']=self.global_test_department.name # this department name is already used in global test setup
        res = self.client.post(self.new_department_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_department_with_duplicate_code(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.department_data.copy()
        data['code']=self.global_test_department.code  # this department code is already is used in global test setup
        res = self.client.post(self.new_department_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    # GET - departments 

    def test_authnaticated_user_can_get_departments(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(self.all_departments_url,format='json')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data),1)

    def test_unauthenticated_user_cannot_get_departments(self):
        res = self.client.get(self.all_departments_url,format='json')
        self.assertEqual(res.status_code, 401)

    # GET - single department by id
    def test_authenticated_user_can_get_a_department(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(reverse(
            self.single_department_url_name,kwargs={'id':self.global_test_department.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data["id"],str(self.global_test_department.id))

    def test_unauthenticated_user_cannot_get_a_department(self):
        res = self.client.get(reverse(
            self.single_department_url_name,kwargs={'id':self.global_test_department.id}
        ),format='json')
        self.assertEqual(res.status_code,401)

    def test_cannot_get_a_department_with_invalid_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(reverse(
            self.single_department_url_name,kwargs={'id':'error_id'}
        ),format='json')
        self.assertEqual(res.status_code,404)

    