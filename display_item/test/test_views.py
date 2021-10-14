from display_item.models import DisplayItem
from django.urls.base import reverse
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    #POST - new display item

    # authenticated user=Lab Manager

    def test_authenticated_user_can_create_display_items(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_display_item_url,self.display_item_data,format='multipart')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')
        self.assertEqual(res.data["name"],self.display_item_data["name"])
    
    def test_authenticated_other_users_cannot_create_display_items(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_display_item_url,self.display_item_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_cannot_create_display_item_without_name(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['name']=""
        res=self.client.post(self.new_display_item_url,data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_display_item_without_description(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['description']=""
        res=self.client.post(self.new_display_item_url,data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_display_item_creation_must_fail_if_item_category_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['item_category']='123'  #Invalid item category Id
        res=self.client.post(self.new_display_item_url,data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_display_item_without_item_category(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['item_category']=""  #Invalid item category Id
        res=self.client.post(self.new_display_item_url,data,format='multipart')
        self.assertEqual(res.status_code,400)

    #GET - display items

    def test_authenticated_user_can_get_display_items(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(self.all_display_items_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)

    def test_unauthenticated_user_cannot_get_display_items(self):
        res=self.client.get(self.all_display_items_url,format='json')
        self.assertEqual(res.status_code,401)
    
    #GET - single display item by id

    def test_authenticated_user_can_get_display_item(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.single_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['id'],str(self.global_test_display_item_one.id))
    
    def test_unauthenticated_user_cannot_get_display_item(self):
        res=self.client.get(reverse(
            self.single_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_a_display_item_with_invalid_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.single_display_item_url_name,kwargs={'id':'error_id'}
        ),format='json')
        self.assertEqual(res.status_code,404)
    
    # GET filtered display item of a specific item category

    def test_authenticated_user_can_get_display_items_of_a_item_category(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.display_items_of_a_item_category_url_name,kwargs={'item_category_id':self.global_test_item_category.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_display_items_of_a_item_category(self):
        res=self.client.get(reverse(
            self.display_items_of_a_item_category_url_name,kwargs={'item_category_id':self.global_test_item_category.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_display_items_if_item_category_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.display_items_of_a_item_category_url_name,kwargs={'item_category_id':"123"}
        ),format='json')
        self.assertEqual(res.status_code,400)
    
    # GET filtered display item of a specific lab

    def test_authenticated_user_can_get_display_items_of_a_lab(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.display_items_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab_two.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)
    
    def test_unauthenticated_user_cannot_get_display_items_of_a_lab(self):
        res=self.client.get(reverse(
            self.display_items_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_display_items_of_a_lab_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.display_items_of_a_lab_url_name,kwargs={'lab_id':"error_id"}
        ),format='json')
        self.assertEqual(res.status_code,400)

# Edit display item tests KEEP THESE TESTS AT LAST

    def test_authenticated_lab_manager_can_edit_display_item_belong_to_his_her_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.put(reverse(
            self.edit_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),self.display_item_edit_data,format='multipart')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['name'],DisplayItem.objects.get(id=self.global_test_display_item_one.id).name)
    
    def test_authenticated_lab_manager_cannot_edit_display_item_doesnt_belong_to_his_her_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager_two)
        res=self.client.put(reverse(
            self.edit_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),self.display_item_edit_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_authenticated_other_user_cannot_edit_display_item(self):
        self.client.force_authenticate(user=self.global_test_lab_assistant)
        res=self.client.put(reverse(
            self.edit_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),self.display_item_edit_data,format='multipart')
        self.assertEqual(res.status_code,403)
    
    def test_unauthenticated_user_cannot_edit_display_item(self):
        res=self.client.put(reverse(
            self.edit_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),self.display_item_edit_data,format='multipart')
        self.assertEqual(res.status_code,401)
    
    def test_description_cannot_be_empty(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_edit_data.copy()
        data['description']=""
        res=self.client.put(reverse(
            self.edit_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),data,format='multipart')
        self.assertEqual(res.status_code,400)
    
    def test_name_cannot_be_empty(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_edit_data.copy()
        data['name']=""
        res=self.client.put(reverse(
            self.edit_display_item_url_name,kwargs={'id':self.global_test_display_item_one.id}
        ),data,format='multipart')
        self.assertEqual(res.status_code,400)

    
    