from django.urls.base import reverse
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    #POST - new display item

    # authenticated user=Lab Manager

    def test_authenticated_user_can_create_display_items(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_display_item_url,self.display_item_data,format='json')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')
        self.assertEqual(res.data["name"],self.display_item_data["name"])
    
    def test_authenticated_other_users_cannot_create_display_items(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_display_item_url,self.display_item_data,format='json')
        self.assertEqual(res.status_code,403)
    
    def test_cannot_create_display_item_without_name(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['name']=""
        res=self.client.post(self.new_display_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_display_item_without_description(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['description']=""
        res=self.client.post(self.new_display_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_display_item_creation_must_fail_if_lab_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['lab']='123'  #Invalid Lab Id
        res=self.client.post(self.new_display_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_display_item_without_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['lab']="" 
        res=self.client.post(self.new_display_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_display_item_creation_must_fail_if_item_category_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['item_category']='123'  #Invalid item category Id
        res=self.client.post(self.new_display_item_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_cannot_create_display_item_without_item_category(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.display_item_data.copy()
        data['item_category']=""  #Invalid item category Id
        res=self.client.post(self.new_display_item_url,data,format='json')
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


    
    