from django.urls.base import reverse
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    # Login Tests

    def test_admin_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.admin_login_data,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.admin_login_data['email'])
        self.assertIsNotNone(res.data['token'])

    def test_lab_manager_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.lab_manager_login_data,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.lab_manager_login_data['email'])
        self.assertIsNotNone(res.data['other_details']['lab']['id'])
        self.assertIsNotNone(res.data['token'])

    def test_lab_assistant_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.lab_assistant_login_data,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.lab_assistant_login_data['email'])
        self.assertIsNotNone(res.data['other_details']['lab']['id'])
        self.assertIsNotNone(res.data['token'])

    def test_student_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.student_login_data,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.student_login_data['email'])
        self.assertIsNotNone(res.data['other_details']['student_id'])
        self.assertIsNotNone(res.data['token'])
    
    def test_lecturer_can_login_with_email_and_password(self):
        res = self.client.post(self.login_url,self.lecturer_login_data,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.lecturer_login_data['email'])
        self.assertIsNotNone(res.data['other_details']['lecturer_id'])
        self.assertIsNotNone(res.data['other_details']['permitted_labs'])
        self.assertIsNotNone(res.data['token'])

    def test_blocked_user_cannot_login(self):
        res = self.client.post(self.login_url,self.blocked_student_login_data,format="multipart")
        self.assertEqual(res.status_code, 401)

    def test_cannot_login_using_invalid_email(self):
        data = self.admin_login_data.copy()
        data['email'] ="error@gmail.com"
        res = self.client.post(self.login_url,data,format="multipart")
        self.assertEqual(res.status_code, 401)
    
    def test_cannot_login_using_invalid_password(self):
        data = self.admin_login_data.copy()
        data['password'] ="pass"
        res = self.client.post(self.login_url,data,format="multipart")
        self.assertEqual(res.status_code, 401)
    
    # refresh auth tests
    def test_admin_can_refresh_auth_using_valid_token(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.global_test_admin.email)
        

    def test_lab_manager_can_refresh_auth_using_valid_token(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.global_test_lab_manager.email)
        self.assertIsNotNone(res.data['other_details']['lab']['id'])
        

    def test_lab_assistant_can_refresh_auth_using_valid_token(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.global_test_lab_assistant.email)
        self.assertIsNotNone(res.data['other_details']['lab']['id'])
        

    def test_student_can_refresh_auth_using_valid_token(self):
        self.client.force_authenticate(user=self.global_test_student)
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.global_test_student.email)
        self.assertIsNotNone(res.data['other_details']['student_id'])
        
    
    def test_lecturer_can_refresh_auth_using_valid_token(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'],self.global_test_lecturer.email)
        self.assertIsNotNone(res.data['other_details']['lecturer_id'])
        self.assertIsNotNone(res.data['other_details']['permitted_labs'])
    
    def test_can_not_refresh_auth_with_invalid_or_empty_token(self):
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 401)
    
    def test_blocked_user_cannot_refresh_auth(self):
        self.client.force_authenticate(user=self.global_blocked_student)
        res = self.client.get(self.refresh_auth_url,format="multipart")
        self.assertEqual(res.status_code, 401)
        

    # Change password tests 

    def test_authenticated_users_can_change_their_password(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res_one = self.client.post(self.change_password_url,self.admin_change_password_data,format="multipart")
        self.assertEqual(res_one.status_code, 200)
        res_two = self.client.post(self.change_password_url,self.admin_change_back_password_data,format="multipart") # to change back the password to keep global test data consistent
        self.assertEqual(res_two.status_code, 200)

    def test_unauthenticated_users_can_not_change_password(self):
        res = self.client.post(self.change_password_url,self.admin_change_password_data,format="multipart")
        self.assertEqual(res.status_code, 401)

    def test_current_password_should_be_provided_change_to_a_new_one(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.admin_change_password_data.copy()
        data["current_password"] = ""
        res = self.client.post(self.change_password_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_current_password_should_be_correct_to_change_to_a_new_one(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.admin_change_password_data.copy()
        data["current_password"] = "123"
        res = self.client.post(self.change_password_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_new_password_should_be_greater_than_8_characters(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.admin_change_password_data.copy()
        data["new_password"] = "#newPas"
        res = self.client.post(self.change_password_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_new_password_should_be_less_than_31_characters(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.admin_change_password_data.copy()
        data["new_password"] = "#newPas#newPas#newPas#newPas#new"
        res = self.client.post(self.change_password_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_new_password_can_not_be_all_numeric_value(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.admin_change_password_data
        data['new_password'] ="12345"
        res = self.client.post(self.change_password_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_new_password_can_not_be_too_common(self):
        self.client.force_authenticate(user=self.global_test_admin)
        data = self.admin_change_password_data
        data['new_password'] ="password"
        res = self.client.post(self.change_password_url,data,format="multipart")
        self.assertEqual(res.status_code, 400)

    # Update Profile Tests

    def test_authenticated_users_can_change_their_profile_details(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.patch(self.update_profile_url,self.update_profile_data,format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["first_name"],self.update_profile_data["first_name"])
        self.assertEqual(res.data["last_name"],self.update_profile_data["last_name"])
        self.assertEqual(res.data["contact_number"],self.update_profile_data["contact_number"])
    
    def test_unauthenticated_users_can_not_edit_profile(self):
        res = self.client.patch(self.update_profile_url,self.update_profile_data,format="multipart")
        self.assertEqual(res.status_code, 401)
    
    def test_authenticated_users_can_change_any_field_without_changing_others(self):
        self.client.force_authenticate(user=self.global_test_admin)
        contact_number = "0753462786"
        res = self.client.patch(self.update_profile_url,{"contact_number": contact_number},format="multipart")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["contact_number"],contact_number)
    
    def test_contact_number_can_only_contain_digits(self):
        self.client.force_authenticate(user=self.global_test_admin)
        contact_number = "07534627ae"
        res = self.client.patch(self.update_profile_url,{"contact_number": contact_number},format="multipart")
        self.assertEqual(res.status_code, 400)
    
    def test_contact_number_if_given_must_be_minimum_6_digits(self):
        self.client.force_authenticate(user=self.global_test_admin)
        contact_number = "075"
        res = self.client.patch(self.update_profile_url,{"contact_number": contact_number},format="multipart")
        self.assertEqual(res.status_code, 400)

    def test_contact_number_if_given_must_be_maximum_15_digits(self):
        self.client.force_authenticate(user=self.global_test_admin)
        contact_number = "0753456253425346"
        res = self.client.patch(self.update_profile_url,{"contact_number": contact_number},format="multipart")
        self.assertEqual(res.status_code, 400)

    # Tests to block, unblock user
    def test_admin_can_block_unblock_other_users(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.put(reverse(self.user_block_url_name,kwargs={'id':self.global_test_student.id}),{"blocked": "true"},format="multipart")
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data["blocked"],True)
        res = self.client.put(reverse(self.user_block_url_name,kwargs={'id':self.global_test_student.id}),{"blocked": "false"},format="multipart")
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data["blocked"],False)

    def test_unauthenticated_users_can_not_block_users(self):
        res = self.client.put(reverse(self.user_block_url_name,kwargs={'id':self.global_test_student.id}),{"blocked": "true"},format="multipart")
        self.assertEqual(res.status_code,401)

    def test_authenticated_adminns_can_not_block_other_admins(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.put(reverse(self.user_block_url_name,kwargs={'id':self.global_test_admin_two.id}),{"blocked": "true"},format="multipart")
        self.assertEqual(res.status_code,400)

    def test_can_not_block_user_with_invalid_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.put(reverse(self.user_block_url_name,kwargs={'id':"456543"}),{"blocked": "true"},format="multipart")
        self.assertEqual(res.status_code,404)
    
    def test_to_block_value_must_be_a_boolen(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res = self.client.put(reverse(self.user_block_url_name,kwargs={'id':self.global_test_student.id}),{"blocked": "rtye"},format="multipart")
        self.assertEqual(res.status_code,400)
    
