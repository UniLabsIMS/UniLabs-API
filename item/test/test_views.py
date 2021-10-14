from django.http import request
from display_item.models import DisplayItem
from django.urls.base import reverse

from request.models import RequestItem, RequestState
from .test_setup import TestSetup
from django.db import transaction
from item.models import Item, LogState, State
import copy

class TestViews(TestSetup):
    #POST - new item creation

    #authenticated user=Lab Manager and Lab assistant

    def test_authenticated_LabManager_can_create_items(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_item_url,self.item_data,format='multipart')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')

    def test_authenticated_LabAssistant_can_create_items(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.post(self.new_item_url,self.item_data,format='multipart')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')

    def test_authenticated_other_user_cannot_create_items(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_item_url,self.item_data,format='multipart')
        self.assertEqual(res.status_code,403)
        self.assertIsNotNone('id')
    
    def test_item_creation_must_fail_if_display_item_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        data=self.item_data.copy()
        data['display_item']='123'  #Invalid display item Id
        res=self.client.post(self.new_item_url,data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_item_without_display_item(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.item_data.copy()
        data['display_item']=""  #Invalid display item Id
        res=self.client.post(self.new_item_url,data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_display_item_count_increase_by_creation_of_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        data_1=self.item["display_item"].item_count
        res=self.client.post(self.new_item_url,self.item_data,format='multipart')
        data_2=DisplayItem.objects.get(id=res.data['display_item']).item_count
        self.assertEqual(data_1+1,data_2)
    
    #GET - items

    def test_authenticated_user_can_get_items(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(self.all_items_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)

    def test_unauthenticated_user_cannot_get_items(self):
        res=self.client.get(self.all_items_url,format='json')
        self.assertEqual(res.status_code,401)
    
    #GET - single item by id

    def test_authenticated_user_can_get_item(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(
            self.single_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['id'],str(self.global_test_item_one.id))
    
    def test_unauthenticated_user_cannot_get_item(self):
        res=self.client.get(reverse(
            self.single_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_a_item_with_invalid_id(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(
            self.single_item_url_name,kwargs={'id':'error_id'}
        ),format='json')
        self.assertEqual(res.status_code,404)
    
    # GET filtered item of a specific display item

    def test_authenticated_user_can_get_items_of_a_display_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.items_of_a_display_item_url_name,kwargs={'display_item_id':self.global_test_display_item_one.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_items_of_a_display_item(self):
        res=self.client.get(reverse(
            self.items_of_a_display_item_url_name,kwargs={'display_item_id':self.global_test_display_item_two.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_items_if_display_item_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.items_of_a_display_item_url_name,kwargs={'display_item_id':"123"}
        ),format='json')
        self.assertEqual(res.status_code,400)

    # GET filtered item of a specific item category

    def test_authenticated_user_can_get_items_of_an_item_category(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.items_of_an_item_category_url_name,kwargs={'item_category_id':self.global_test_item_category.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_items_of_an_item_category(self):
        res=self.client.get(reverse(
            self.items_of_an_item_category_url_name,kwargs={'item_category_id':self.global_test_item_category_two.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_items_if_display_item_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.items_of_an_item_category_url_name,kwargs={'item_category_id':"error_id"}
        ),format='json')
        self.assertEqual(res.status_code,400)
    
    # GET filtered item of a specific lab

    def test_authenticated_user_can_get_items_of_a_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.items_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab_two.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_items_of_a_lab(self):
        res=self.client.get(reverse(
            self.items_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab_two.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_items_if_lab_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.get(reverse(
            self.items_of_a_lab_url_name,kwargs={'lab_id':"error_id"}
        ),format='json')
        self.assertEqual(res.status_code,400)


    # Delete Item

    def test_authenticated_LabManager_can_delete_items(self):
        # create an item to delete
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res_created=self.client.post(self.new_item_url,self.item_data,format='multipart')
        # then delete it
        item_count_parent_b4= DisplayItem.objects.get(id = self.item_data["display_item"]).item_count
        res=self.client.delete(reverse(
            self.delete_item_url_name,kwargs={'id':res_created.data['id']}
        ),format='multipart')
        item_count_parent_after= DisplayItem.objects.get(id = self.item_data["display_item"]).item_count
        self.assertEqual(res.status_code,204)
        self.assertEqual(item_count_parent_b4,item_count_parent_after+1)
    
    def test_authenticated_LabAssistant_can_delete_items(self):
        # create an item to delete
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res_created=self.client.post(self.new_item_url,self.item_data,format='multipart')
        # then delete it
        item_count_parent_b4= DisplayItem.objects.get(id = self.item_data["display_item"]).item_count
        res=self.client.delete(reverse(
            self.delete_item_url_name,kwargs={'id':res_created.data['id']}
        ),format='multipart')
        item_count_parent_after= DisplayItem.objects.get(id = self.item_data["display_item"]).item_count
        self.assertEqual(res.status_code,204)
        self.assertEqual(item_count_parent_b4,item_count_parent_after+1)
    
    def test_authenticated_LabAssistant_can_not_delete_items_of_other_lab(self):
        # create an item to delete
        self.client.force_authenticate(user=self.global_test_lab_assistant_two)
        res_created=self.client.post(self.new_item_url,self.item_data,format='multipart')
        # then delete it
        self.client.force_authenticate(user=self.global_test_student)
        res=self.client.delete(reverse(
            self.delete_item_url_name,kwargs={'id':res_created.data['id']}
        ),format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_authenticated_Other_Users_can_not_delete_items(self):
        # create an item to delete
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res_created=self.client.post(self.new_item_url,self.item_data,format='multipart')
        # then delete it
        self.client.force_authenticate(user=self.global_test_student)
        res=self.client.delete(reverse(
            self.delete_item_url_name,kwargs={'id':res_created.data['id']}
        ),format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_Users_can_not_delete_items(self):
        # create an item to delete
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res_created=self.client.post(self.new_item_url,self.item_data,format='multipart')
        # then delete it
        self.client.force_authenticate(user=None)
        res=self.client.delete(reverse(
            self.delete_item_url_name,kwargs={'id':res_created.data['id']}
        ),format='multipart')
        self.assertEqual(res.status_code,401)

    def test_can_not_delete_non_existing_items(self):
        # create an item to delete
        self.client.force_authenticate(user=self.global_test_lab_manager)
        # then delete it
        res=self.client.delete(reverse(
            self.delete_item_url_name,kwargs={'id':'65254675'}
        ),format='multipart')
        self.assertEqual(res.status_code,404)
    
    #POST temporary borrow
    def test_authenticated_Lab_Assistant_can_handover_items_temporally(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.student_data,format='multipart')
        self.assertEqual(res.status_code,200)
    
    def test_authenticated_other_user_cannot_handover_items_temporally(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.student_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_handover_items_temporally(self):
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.student_data,format='multipart')
        self.assertEqual(res.status_code,401)
    
    def test_authenticated_Lab_Assistant_cannot_handover_items_temporally_in_other_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant_two)
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.student_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_item_id_cannot_be_invalid_in_temp_handover(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':"Invalid_id"}
        ),self.student_data,format='multipart')
        self.assertEqual(res.status_code,404)
    
    def test_student_id_cannot_be_invalid_in_temp_handover(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        data=self.student_data.copy()
        data['student_uuid']='invalid'
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_temp_handover_item_cannot_be_other_state_than_available(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        item=self.global_test_item_one
        item.state=State.TEMP_BORROWED
        item.save()
        res=self.client.post(reverse(
            self.temporary_handover_url_name,kwargs={'id':item.id}
        ),self.student_data,format='multipart')
        self.assertEqual(res.status_code,400)
        item.state = State.AVAILABLE
        item.save()

#GET - all-borrow-logs

    def test_authenticated_user_can_get_borrow_logs(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(self.all_borrow_logs_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),4)
    
    def test_unauthenticated_user_cannot_get_borrow_logs(self):
        res=self.client.get(self.all_borrow_logs_url,format='json')
        self.assertEqual(res.status_code,401)

#GET - all-borrow-logs-of-lab
    def test_authenticated_user_can_get_borrow_logs_of_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.all_borrow_logs_of_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),3)
    
    def test_unauthenticated_user_cannot_get_borrow_logs_of_lab(self):
        res=self.client.get(reverse(self.all_borrow_logs_of_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_borrow_log_lab_filter_should_fail_for_invalid_lab_id(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.all_borrow_logs_of_lab_url_name,kwargs={'lab_id':"Blah"}),format='json')
        self.assertEqual(res.status_code,400)

#GET - all-borrow-logs-of-student
    def test_authenticated_user_can_get_borrow_logs_of_student(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.all_borrow_logs_of_student_url_name,kwargs={'student_id':self.global_test_student.id}),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),3)
    
    def test_unauthenticated_user_cannot_get_borrow_logs_of_student(self):
        res=self.client.get(reverse(self.all_borrow_logs_of_student_url_name,kwargs={'student_id':self.global_test_student.id}),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_borrow_log_student_filter_should_fail_for_invalid_student_id(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.all_borrow_logs_of_student_url_name,kwargs={'student_id':"Blah"}),format='json')
        self.assertEqual(res.status_code,400)

#GET - curently-borrowed-logs-of-lab
    def test_authenticated_user_can_get_currently_borrowed_list_of_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.currently_borrowed_from_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(res.data),2)
    
    def test_unauthenticated_user_cannot_get_currently_borrowed_list_of_lab(self):
        res=self.client.get(reverse(self.currently_borrowed_from_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_authenticated_user_can_not_get_currently_borrowed_list_of_lab_is_id_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.currently_borrowed_from_lab_url_name,kwargs={'lab_id':"Blah"}),format='json')
        self.assertEqual(res.status_code,400)

#GET - curently-borrowed-logs-of-lab
    def test_authenticated_user_can_get_currently_borrowed_list_by_student(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.currently_borrowed_by_student_url_name,kwargs={'student_id':self.global_test_student.id}),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(res.data),2)
    
    def test_unauthenticated_user_cannot_get_currently_borrowed_list_by_student(self):
        res=self.client.get(reverse(self.currently_borrowed_by_student_url_name,kwargs={'student_id':self.global_test_student.id}),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_authenticated_user_can_not_get_currently_borrowed_list_by_student_is_id_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.get(reverse(self.currently_borrowed_by_student_url_name,kwargs={'student_id':"Blah"}),format='json')
        self.assertEqual(res.status_code,400)
#PUT returning item

    def test_authenticated_lab_assistant_can_receive_return_item_belongs_to_his_her_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),{},format='multipart')
        self.assertEqual(res.status_code,200)
    
    def test_authenticated_lab_assistant_cannot_receive_return_item_does_not_belongs_to_her_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant_two)
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),{},format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_authenticated_other_user_cannot_receive_return_item(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),{},format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_receive_return_item(self):
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),{},format='multipart')
        self.assertEqual(res.status_code,401)
    
    def test_return_item_id_cannot_be_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':"invalid_id"}
        ),{},format='multipart')
        self.assertEqual(res.status_code,404)
    
    def test_return_item_should_not_be_other_state_rather_than_BORROWED_or_TEMP_BORROWED(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        borrow_log=self.global_test_borrow_log_one
        borrow_log.state=LogState.RETURNED
        borrow_log.save()
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),{},format='multipart')
        self.assertEqual(res.status_code,400)
        borrow_log.state=LogState.TEMP_BORROWED
        borrow_log.save()
    
    def test_return_item_should_not_be_invalid_state(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        borrow_log=self.global_test_borrow_log_one
        borrow_log.state="Invalid State"
        borrow_log.save()
        res=self.client.put(reverse(
            self.return_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),{},format='multipart')
        self.assertEqual(res.status_code,400)
        borrow_log.state=LogState.TEMP_BORROWED
        borrow_log.save()
    



# Edit item 

    def test_authenticated_lab_assistant_can_edit_item_doesnt_belong_to_his_her_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.put(reverse(
            self.edit_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.edit_item_data,format='multipart')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['state'],State.BORROWED)
    
    def test_authenticated_lab_assistant_cannot_edit_item_doesnt_belong_to_his_her_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant_two)
        res=self.client.put(reverse(
            self.edit_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.edit_item_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_authenticated_other_user_cannot_edit_item(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.put(reverse(
            self.edit_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.edit_item_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_other_user_cannot_edit_item(self):
        res=self.client.put(reverse(
            self.edit_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.edit_item_data,format='multipart')
        self.assertEqual(res.status_code,401)
    
    def test_item_state_cannot_be_invalid_state(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        data=self.edit_item_data.copy()
        data['state']="invalid_state"
        res=self.client.put(reverse(
            self.edit_item_url_name,kwargs={'id':self.global_test_item_one.id}
        ),data,format='multipart')
        self.assertEqual(res.status_code,400)
    

    # POST handover items test
    def test_authenticated_Lab_Assistant_can_handover_items(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,200)
    
    def test_authenticated_other_user_cannot_hand_over_items(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_hand_over_items(self):
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,401)
    
    def test_item_id_should_not_be_invalid_while_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':"invalid id"}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,404)
    
    def test_item_state_cannot_be_other_state_than_AVAILABLE_state_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        item=self.global_test_item_one
        item.state=State.BORROWED
        item.save()
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':item.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
        item.state=State.AVAILABLE
        item.save()
    
    def test_item_state_cannot_be_invalid_state_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        item=self.global_test_item_one
        item.state="Invalid State"
        item.save()
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':item.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
        item.state=State.AVAILABLE
        item.save()
    
    def test_display_item_of_request_item_and_display_item_of_item_cannot_be_different(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        handover_data=self.item_handover_data.copy()
        handover_data['request_item_id']=self.global_test_request_item_two.id
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_request_item_state_cannot_be_other_state_than_APPROVED_state_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        request_item=self.global_test_request_item_one
        request_item.state=RequestState.DECLINED
        request_item.save()
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
        request_item.state=RequestState.APPROVED
        request_item.save()
    
    def test_request_item_quantity_cannot_be_less_than_or_equal_to_zero_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        request_item=self.global_test_request_item_one
        request_item.quantity=0
        request_item.save()
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),self.item_handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
        request_item.quantity=1
        request_item.save()
    
    def test_due_date_should_not_be_any_day_before_today_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        handover_data=self.item_handover_data.copy()
        handover_data['due_date']='2020-01-31'
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_request_item_id_cannot_be_invalid_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        handover_data=self.item_handover_data.copy()
        handover_data['request_item_id']='Invalid id'
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_due_date_cannot_be_invalid_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        handover_data=self.item_handover_data.copy()
        handover_data['due_date']='Invalid date'
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_request_item_id_cannot_be_empty_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        handover_data=self.item_handover_data.copy()
        handover_data['request_item_id']=''
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_due_date_cannot_be_empty_when_hand_over_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        handover_data=self.item_handover_data.copy()
        handover_data['due_date']=''
        res=self.client.post(reverse(
            self.item_handover_url_name,kwargs={'id':self.global_test_item_one.id}
        ),handover_data,format='multipart')
        self.assertEqual(res.status_code,400)
    

    
