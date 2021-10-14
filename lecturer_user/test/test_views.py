from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # POST - New Lecturer

    def test_authenticated_admin_can_register_new_lecturers(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_lecturer_url,self.lecturer_data,format="multipart")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['lecturer_id'],self.lecturer_data['lecturer_id'])
        self.assertEqual(res.data['email'],self.lecturer_data['email'])

    def test_unauthenticated_user_cannot_add_lecturers(self):
        res = self.client.post(self.new_lecturer_url,self.lecturer_data,format="multipart")
        self.assertEqual(res.status_code, 401)

    def test_authenticated_other_users_cannot_register_new_lecturers(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.post(self.new_lecturer_url,self.lecturer_data,format="multipart")
        self.assertEqual(res.status_code, 403)

    def test_cannot_add_lecturer_with_no_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["email"]=""
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lecturer_with_invalid_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["email"]="test"
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lecturer_with_in_use_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["email"]=self.global_test_lecturer.email
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_lecturer_with_no_lecturer_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["lecturer_id"]=""
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_add_lecturer_with_duplicate_lecturer_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["lecturer_id"]=self.global_test_lecturer.lecturer_id
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
        
    def test_cannot_add_lecturer_with_invalid_lab_ids(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["permitted_labs"]= ["234"]
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_add_lecturer_with_duplicate_lab_ids(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["permitted_labs"].append(self.global_test_lab.id)
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_add_lecturer_with_lab_ids_not_under_department(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lecturer_data.copy()
        data["permitted_labs"].append(self.global_test_lab_two.id)
        res = self.client.post(self.new_lecturer_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    # GET - all students

    def test_authenticated_admin_users_can_get_a_list_of_lecturers(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(self.all_lecturers_url,data_format="json")
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_users_cannot_get_list_of_lecturers(self):
        res = self.client.get(self.all_lecturers_url,data_format="json")
        self.assertEqual(res.status_code,401)

    def test_authenticated_non_admin_users_cannot_get_list_of_lecturers(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.get(self.all_lecturers_url,data_format="json")
        self.assertEqual(res.status_code,403)