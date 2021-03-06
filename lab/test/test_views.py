from django.urls.base import reverse
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    #POST - new lab
    def test_authenticated_admin_can_create_labs(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.new_lab_url,self.lab_data,format="multipart")
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone('id')
    
    def test_authenticated_other_users_cannot_create_department(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_lab_url,self.lab_data,format="multipart")
        self.assertEqual(res.status_code,403)
    
    def test_cannot_create_lab_without_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data=self.lab_data.copy()
        data['name']=""
        res=self.client.post(self.new_lab_url,data,format='multipart')
        self.assertEqual(res.status_code,400)

    def test_cannot_create_lab_with_duplicate_name(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data=self.lab_data.copy()
        data['name']=self.global_test_lab.name
        res=self.client.post(self.new_lab_url,data,format='multipart')
        self.assertEqual(res.status_code,400)

    def test_lab_creation_must_fail_if_department_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.lab_data.copy()
        data['department'] = '123' # Invalid department id
        res = self.client.post(self.new_lab_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_lab_without_department(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data=self.lab_data.copy()
        data['department']=""
        res=self.client.post(self.new_lab_url,data,format="multipart")
        self.assertEqual(res.status_code,400)
        
    #GET - labs

    def test_authenticated_user_can_get_labs(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(self.all_labs_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_labs(self):
        res=self.client.get(self.all_labs_url,format='json')
        self.assertEqual(res.status_code,401)
    
    #GET - single lab by id

    def test_authenticated_user_can_get_lab(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.single_lab_url_name,kwargs={'id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['id'],str(self.global_test_lab.id))
        
    def test_unauthenticated_user_cannot_get_a_lab(self):
        res = self.client.get(reverse(
            self.single_lab_url_name,kwargs={'id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_a_lab_with_invalid_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.single_lab_url_name,kwargs={'id':'error_id'}
        ),format='json')
        self.assertEqual(res.status_code,404)
    
    # GET filtered labs of a specific department

    def test_authenticated_user_can_get_labs_of_a_department(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(
            self.labs_of_a_department_url_name,kwargs={'department_id':self.global_test_department.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_labs_of_a_department(self):
        res=self.client.get(reverse(
            self.labs_of_a_department_url_name,kwargs={'department_id':self.global_test_department.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test__cannot_get_labs_of_a_department_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(
            self.labs_of_a_department_url_name,kwargs={'department_id':"error_id"}
        ),format='json')
        self.assertEqual(res.status_code,400)
    
    # GET lab report
    def test_authenticated_user_can_get_lab_report(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.lab_report_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
    
    def test_unauthenticated_user_cannot_get_lab_report(self):
        res=self.client.get(reverse(
            self.lab_report_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_authenticated_user_cannot_get_lab_report_with_invalid_lab_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.lab_report_url_name,kwargs={'lab_id':'invalid id'}
        ),format='json')
        self.assertEqual(res.status_code,400)
    
    # Assign lecturer to lab KEEP AT END

    def test_admin_can_assign_new_lecturers_to_labs(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.post(self.assign_lec_to_lab_url,self.assign_lecs_to_lab_data,format="multipart")
        self.assertEqual(res.status_code, 200)
    
    def test_admin_can_not_assign_invalid_lecturers_to_labs(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.assign_lecs_to_lab_data.copy()
        data['lecturers'] = ["Invalid id"]
        res = self.client.post(self.assign_lec_to_lab_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_admin_can_not_assign_already_assigned_lecturers_to_labs(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.assign_lecs_to_lab_data.copy()
        data['lecturers'].append(self.global_test_lecturer.id)
        res = self.client.post(self.assign_lec_to_lab_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_unauthenticated_users_can_not_assigned_lecturers_to_labs(self):
        res = self.client.post(self.assign_lec_to_lab_url,self.assign_lecs_to_lab_data,format="multipart")
        self.assertEqual(res.status_code, 401)
    
    def test_authenticated_other_users_can_not_assigned_lecturers_to_labs(self):
        res = self.client.post(self.assign_lec_to_lab_url,self.assign_lecs_to_lab_data,format="multipart")
        self.assertEqual(res.status_code, 401)





    
