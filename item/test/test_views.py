from display_item.models import DisplayItem
from django.urls.base import reverse
from .test_setup import TestSetup
from django.db import transaction

class TestViews(TestSetup):
    #POST - new item creation

    #authenticated user=Lab Manager and Lab assistant

    def test_authenticated_LabManager_can_create_items(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_item_url,self.item_data,format='json')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')

    def test_authenticated_LabAssistant_can_create_items(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.post(self.new_item_url,self.item_data,format='json')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')

    def test_authenticated_other_user_cannot_create_items(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_item_url,self.item_data,format='json')
        self.assertEqual(res.status_code,403)
        self.assertIsNotNone('id')
    
    def test_item_creation_must_fail_if_display_item_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        data=self.item_data.copy()
        data['display_item']='123'  #Invalid display item Id
        res=self.client.post(self.new_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_item_without_display_item(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.item_data.copy()
        data['display_item']=""  #Invalid display item Id
        res=self.client.post(self.new_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_display_item_count_increase_by_creation_of_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        data_1=self.item["display_item"].item_count
        res=self.client.post(self.new_item_url,self.item_data,format='json')
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