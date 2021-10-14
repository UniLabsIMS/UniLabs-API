from .test_setup import TestSetup
from django.urls.base import reverse
from request.models import Request
import copy

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

    def test_authenticated_student_can_view_their_new_requests(self):
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
    
    #GET - all requests by lecturer

    def test_authenticated_lecturer_can_view_their_new_requests(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res=self.client.get(self.lecturer_requests_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_view_lecturer_requests(self):
        res=self.client.get(self.lecturer_requests_url,format='json')
        self.assertEqual(res.status_code,401)
    
    def test_authenticated_other_user_cannot_view_lecturer_requests(self):
        self.client.force_authenticate(user=self.global_test_student)
        res=self.client.get(self.lecturer_requests_url,format='json')
        self.assertEqual(res.status_code,403)
    
    #GET - all requests by lab

    def test_authenticated_user_can_get_requests_filter_by_lab(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res=self.client.get(reverse(
            self.requests_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_requests_filter_by_lab(self):
        res=self.client.get(reverse(
            self.requests_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_requests_filter_by_invalid_lab_id(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res=self.client.get(reverse(
            self.requests_of_a_lab_url_name,kwargs={'lab_id':"Invalid id"}
        ),format='json')
        self.assertEqual(res.status_code,400)


    #PUT Approve or Decline Request
    def test_authenticated_lecturer_can_approve_new_request(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res = self.client.put(reverse(self.approve_or_decline_url_name,kwargs={'id':self.global_test_request_one.id}),{"state": "Approved"},format="multipart")
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['state'],"Approved")
    
    def test_authenticated_lecturer_can_decline_new_request(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        res = self.client.put(reverse(self.approve_or_decline_url_name,kwargs={'id':self.global_test_request_one.id}),{"state": "Declined"},format="multipart")
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['state'],"Declined")

    def test_authenticated_lecturer_not_assigned_to_request_can_not_change_state(self):
        self.client.force_authenticate(user=self.global_test_lecturer_two)
        res = self.client.put(reverse(self.approve_or_decline_url_name,kwargs={'id':self.global_test_request_one.id}),{"state": "Approved"},format="multipart")
        self.assertEqual(res.status_code,401)
    
    def test_initial_state_of_request_should_be_new(self):
        self.client.force_authenticate(user=self.global_test_lecturer)
        request=copy.copy(self.global_test_request_one)
        request.state="Approved"
        request.save()
        res = self.client.put(reverse(self.approve_or_decline_url_name,kwargs={'id':request.id}),{"state": "Declined"},format="multipart")
        self.assertEqual(res.status_code,400)
    
    def test_authenticated_other_cannot_approve_or_decline_new_request(self):
        self.client.force_authenticate(user=self.global_test_student)
        res = self.client.put(reverse(self.approve_or_decline_url_name,kwargs={'id':self.global_test_request_one.id}),{"state": "Approved"},format="multipart")
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_approve_or_decline_new_request(self):
        res = self.client.put(reverse(self.approve_or_decline_url_name,kwargs={'id':self.global_test_request_one.id}),{"state": "Approved"},format="multipart")
        self.assertEqual(res.status_code,401)
    
    #GET - filter request item by student and lab

    def test_authenticated_user_can_filter_request_item_by_student_and_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.approved_request_items_url_name,kwargs={'lab_id':self.global_test_lab.id,'student_id':self.global_test_student.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)

    def test_authenticated_other_user_cannot_filter_request_item_by_student_and_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(
            self.approved_request_items_url_name,kwargs={'lab_id':self.global_test_lab.id,'student_id':self.global_test_student.id}
        ),format='json')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_filter_request_item_by_student_and_lab(self):
        res=self.client.get(reverse(
            self.approved_request_items_url_name,kwargs={'lab_id':self.global_test_lab.id,'student_id':self.global_test_student.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_lab_id_and_student_id_cannot_be_invalid_when_filter_item_by_student_and_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.approved_request_items_url_name,kwargs={'lab_id':'invalid_id','student_id':'invalid_id'}
        ),format='json')
        self.assertEqual(res.status_code,400)
    
    #PUT - Clear approved display items

    def test_authenticated_user_can_clear_approved_display_items_from_lab_for_student(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res = self.client.put(reverse(self.clear_approved_request_items_url_name),{"student": self.global_test_student.id,"lab":self.global_test_lab.id},format="multipart")
        self.assertEqual(res.status_code,200)
    
    def test_authenticated_other_user_cannot_clear_approved_display_items_from_lab_for_student(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res = self.client.put(reverse(self.clear_approved_request_items_url_name),{"student": self.global_test_student.id,"lab":self.global_test_lab.id},format="multipart")
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_clear_approved_display_items_from_lab_for_student(self):
        res = self.client.put(reverse(self.clear_approved_request_items_url_name),{"student": self.global_test_student.id,"lab":self.global_test_lab.id},format="multipart")
        self.assertEqual(res.status_code,401)
    


    
    



    
    

    

