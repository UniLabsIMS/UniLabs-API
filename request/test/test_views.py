from .test_setup import TestSetup

class TestViews(TestSetup):
    #POST- New request

    def test_authenticated_student_can_create_new_request(self):
        self.client.force_authenticate(user=self.global_test_student)
        res=self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,201)
    
    def test_authenticated_other_users_cannot_create_new_request(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_create_new_request(self):
        res=self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,401)

    def test_authenticated_student_can_not_have_more_than_one_new_request_for_same_lab(self):
        self.client.force_authenticate(user=self.global_test_student)
        self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        res = self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,400)

    def test_cannot_add_request_with_empty_student_id(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["student"]=""
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_wrong_student_id(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["student"]="wrong id"
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_empty_lecture_id(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["lecturer"]=""
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_wrong_lecture_id(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["lecturer"]="wrong id"
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_non_permitted_lecture_id(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["lecturer"] = self.global_test_lecturer_two.id
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_empty_reason(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["reason"]=""
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_wrong_display_item_id(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["display_items_dict"]={"invalid_display_id":2,"invalid_display_id":2}
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_display_item_ids_of_other_labs(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["display_items_dict"]={str(self.global_test_display_item_one):1,str(self.global_test_display_item_two):1}
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_zero_or_negative_items(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["display_items_dict"][str(self.global_test_display_item_five.id)] = 0
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_excess_items(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["display_items_dict"][str(self.global_test_display_item_five.id)]+=10
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    def test_cannot_add_request_with_non_int_value_for_item_count(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["display_items_dict"][str(self.global_test_display_item_five.id)] = "rf"
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    #GET - all requests by student

    def test_authenticated_student_can_view_their_requests(self):
        self.client.force_authenticate(user=self.global_test_student)
        res=self.client.get(self.student_requests_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_view_student_requests(self):
        res=self.client.get(self.student_requests_url,format='json')
        self.assertEqual(res.status_code,401)
    
    def test_authenticated_other_user_cannot_view_student_requests(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res=self.client.get(self.student_requests_url,format='json')
        self.assertEqual(res.status_code,403)
        self.assertGreaterEqual(len(res.data),1)
    

