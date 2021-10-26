from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ItemCategoryCreateAPIView, ItemCategoryListAPIView, ItemCategoryListByLabAPIView, ItemCategoryRetrieveAPIView, ItemCategoryUpdateAPIView

class TestUrls(SimpleTestCase):

    def test_all_item_categories_url_and_view(self):
        url = reverse('all-item-categories')
        self.assertEqual(resolve(url).func.view_class, ItemCategoryListAPIView)

    def test_single_item_category_url_and_view(self):
        url = reverse('single-item-category',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemCategoryRetrieveAPIView)
    
    def test_new_item_category_url_and_view(self):
        url = reverse('new-item-category')
        self.assertEqual(resolve(url).func.view_class, ItemCategoryCreateAPIView)
    
    def test_update_item_category_url_and_view(self):
        url = reverse('update-item-category',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemCategoryUpdateAPIView)
    
    def test_item_categories_of_a_lab_url_and_view(self):
        url = reverse('item-categories-of-a-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemCategoryListByLabAPIView)