from django.urls.base import reverse
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    #POST - new item category

    # authenticated user=Lab Manager
    def test_authenticated_user_can_create_item_categories(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        res=self.client.post(self.new_item_category_url,self.item_category_data,format='json')
        self.assertEqual(res.status_code,201)
        self.assertIsNotNone('id')
        self.assertEqual(res.data["name"],self.item_category_data["name"])
    
    def test_authenticated_other_users_cannot_create_item_category(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.post(self.new_item_category_url,self.item_category_data,format='json')
        self.assertEqual(res.status_code,403)

    def test_cannot_create_item_category_without_name(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.item_category_data.copy()
        data['name']=""
        res=self.client.post(self.new_item_category_url,data,format='json')
        self.assertEqual(res.status_code,400)

    def test_cannot_create_item_category_without_description(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.item_category_data.copy()
        data['description']=""
        res=self.client.post(self.new_item_category_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    def test_item_category_creation_must_fail_if_lab_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.item_category_data.copy()
        data['lab']='123'  #Invalid Lab Id
        res=self.client.post(self.new_item_category_url,data,format='json')
        self.assertEqual(res.status_code,400)

    def test_cannot_create_item_category_without_lab(self):
        self.client.force_authenticate(user=self.global_test_lab_manager)
        data=self.item_category_data.copy()
        data['lab']=""
        res=self.client.post(self.new_item_category_url,data,format='json')
        self.assertEqual(res.status_code,400)
    
    #GET - item category

    def test_authenticated_user_can_get_item_categories(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(self.all_item_categories_url,format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),1)

    def test_unauthenticated_user_cannot_get_item_categories(self):
        res=self.client.get(self.all_item_categories_url,format='json')
        self.assertEqual(res.status_code,401)

    #GET - single item category by id

    def test_authenticated_user_can_get_item_category(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.single_item_category_url_name,kwargs={'id':self.global_test_item_category.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.data['id'],str(self.global_test_item_category.id))

    def test_unauthenticated_user_cannot_get_a_item_category(self):
        res = self.client.get(reverse(
            self.single_item_category_url_name,kwargs={'id':self.global_test_item_category.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_cannot_get_a_item_category_with_invalid_id(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.single_item_category_url_name,kwargs={'id':'error_id'}
        ),format='json')
        self.assertEqual(res.status_code,404)

    # GET filtered categories of a specific lab

    def test_authenticated_user_can_get_categories_of_a_lab(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.item_categories_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,200)
        self.assertGreaterEqual(len(res.data),2)
    
    def test_unauthenticated_user_cannot_get_categories_of_a_lab(self):
        res=self.client.get(reverse(
            self.item_categories_of_a_lab_url_name,kwargs={'lab_id':self.global_test_lab.id}
        ),format='json')
        self.assertEqual(res.status_code,401)
    
    def test_can_not_get_categories_if_lab_id_is_invalid(self):
        self.client.force_authenticate(user=self.global_test_admin)
        res=self.client.get(reverse(
            self.item_categories_of_a_lab_url_name,kwargs={'lab_id':"123"}
        ),format='json')
        self.assertEqual(res.status_code,400)