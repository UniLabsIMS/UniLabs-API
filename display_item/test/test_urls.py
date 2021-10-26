from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import DisplayItemCreateAPIView,DisplayItemListAPIView,DisplayItemListByLabAPIView,DisplayRetrieveAPIView,DisplayItemUpdateAPIView,DisplayItemListByItemCategoryAPIView


class TestUrls(SimpleTestCase):

    def test_all_display_items_url_and_view(self):
        url = reverse('all-display-items')
        self.assertEqual(resolve(url).func.view_class, DisplayItemListAPIView)

    def test_single_display_item_url_and_view(self):
        url = reverse('single-display-item',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, DisplayRetrieveAPIView)
    
    def test_new_display_item_url_and_view(self):
        url = reverse('new-display-item')
        self.assertEqual(resolve(url).func.view_class, DisplayItemCreateAPIView)
    
    def test_update_display_item_url_and_view(self):
        url = reverse('update-display-item',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, DisplayItemUpdateAPIView)
    
    def test_display_items_of_a_item_category_url_and_view(self):
        url = reverse('display-items-of-a-item-category',kwargs={'item_category_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, DisplayItemListByItemCategoryAPIView)
    
    def test_display_items_of_a_lab_url_and_view(self):
        url = reverse('display-items-of-a-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, DisplayItemListByLabAPIView)