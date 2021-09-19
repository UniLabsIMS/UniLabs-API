from display_item.models import DisplayItem
from django.db import models
from .test_setup import TestSetup
from display_item.models import DisplayItem
from request.models import RequestItem,Request
from django.urls.base import reverse

class TestViews(TestSetup):
    #POST- New request

    def test_authenticated_student_can_create_new_request(self):
        self.client.force_authenticate(user=self.global_test_student)
        # import pdb; pdb.set_trace()
        res=self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,201)
    
    def test_authenticated_other_user_cannot_create_new_request(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_create_new_request(self):
        res=self.client.post(self.new_request_url,self.request_api_view_data,format="json")
        self.assertEqual(res.status_code,401)

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
    
    def test_cannot_add_request_with_excess_items(self):
        self.client.force_authenticate(user=self.global_test_student)
        data=self.request_api_view_data.copy()
        data["display_items_dict"]={str(self.global_test_request_item_one.display_item.id):self.global_test_request_item_one.display_item.item_count+1}
        res=self.client.post(self.new_request_url,data,format="json")
        self.assertEqual(res.status_code,400)
    
    #GET - all requests
    def test_authenticated_user_can_get_a_list_of_requests(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res = self.client.get(self.all_requests_url,data_format="json")
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_authenticated_other_user_cannot_get_a_list_of_requests(self):
        self.client.force_authenticate(user=self.global_test_student)
        res = self.client.get(self.all_requests_url,data_format="json")
        self.assertEqual(res.status_code,403)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_authenticated_other_user_cannot_get_a_list_of_requests(self):
        res = self.client.get(self.all_requests_url,data_format="json")
        self.assertEqual(res.status_code,401)
    

