from django.urls.base import reverse
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # POST - New Student

    def test_authenticated_admin_can_register_new_students(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_student_url,self.student_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['student_id'],self.student_data['student_id'])
        self.assertEqual(res.data['email'],self.student_data['email'])

    def test_unauthenticated_user_cannot_add_students(self):
        res = self.client.post(self.new_student_url,self.student_data,format="json")
        self.assertEqual(res.status_code, 401)

    def test_authenticated_other_users_cannot_register_new_students(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.post(self.new_student_url,self.student_data,format="json")
        self.assertEqual(res.status_code, 403)

    def test_cannot_add_student_with_no_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.student_data.copy()
        data["email"]=""
        res = self.client.post(self.new_student_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_student_with_invalid_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.student_data.copy()
        data["email"]="test"
        res = self.client.post(self.new_student_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_student_with_in_use_email(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.student_data.copy()
        data["email"]=self.global_test_student.email
        res = self.client.post(self.new_student_url,data,format="json")
        self.assertEqual(res.status_code, 400)

    def test_cannot_add_student_with_no_student_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.student_data.copy()
        data["student_id"]=""
        res = self.client.post(self.new_student_url,data,format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_cannot_add_student_with_duplicate_student_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.student_data.copy()
        data["student_id"]=self.global_test_student.student_id
        res = self.client.post(self.new_student_url,data,format="json")
        self.assertEqual(res.status_code, 400)
    
    # GET - all students

    def test_authenticated_admin_users_can_get_a_list_of_students(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(self.all_students_url,data_format="json")
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_users_cannot_get_list_of_students(self):
        res = self.client.get(self.all_students_url,data_format="json")
        self.assertEqual(res.status_code,401)

    def test_authenticated_non_admin_users_cannot_get_list_of_students(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.get(self.all_students_url,data_format="json")
        self.assertEqual(res.status_code,403)
    
    # GET - all student

    def test_authenticated_users_can_get_a_student(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res = self.client.get(reverse(
            self.get_student_url_name,kwargs={'id':self.global_test_student.id}
        ),data_format="json")
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(res.data['id'],str(self.global_test_student.id))
    
    def test_unauthenticated_users_cannot_get_list_of_students(self):
        res = self.client.get(reverse(
            self.get_student_url_name,kwargs={'id':self.global_test_student.id}
        ),data_format="json")
        self.assertEqual(res.status_code,401)

    def test_when_getting_student_invalid_student_id_should_return_404(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.get(reverse(
            self.get_student_url_name,kwargs={'id':"invalid id"}
        ),data_format="json")
        self.assertEqual(res.status_code,404)