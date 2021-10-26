from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import BorrowLogListofLabAPIView, BorrowLogListofStudentAPIView, CurrentBorrowedItemListofLabAPIView, CurrentBorrowedItemListofStudentAPIView, HandOverItemAPIView, ItemCreateAPIView, ItemDeleteAPIView,ItemListByLabAPIView, ItemListByItemCategoryAPIView,ItemUpdateAPIView,ItemListAPIView,ItemListByDisplayItemAPIView,ItemRetriveAPIView,TemporaryHandOverItemAPIView,ReturnItemAPIView,BorrowLogListAPIView

class TestUrls(SimpleTestCase):

    def test_all_items_url_and_view(self):
        url = reverse('all-items')
        self.assertEqual(resolve(url).func.view_class,ItemListAPIView)

    def test_single_item_url_and_view(self):
        url = reverse('single-item',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,ItemRetriveAPIView)
    
    def test_new_item_url_and_view(self):
        url = reverse('new-item')
        self.assertEqual(resolve(url).func.view_class, ItemCreateAPIView)
    
    def test_update_item_url_and_view(self):
        url = reverse('update-item',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemUpdateAPIView)
    
    def test_delete_item_url_and_view(self):
        url = reverse('delete-item',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemDeleteAPIView)
    
    def test_items_of_a_display_item_url_and_view(self):
        url = reverse('items-of-a-display-item',kwargs={'display_item_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemListByDisplayItemAPIView)
    
    def test_items_of_an_item_category_url_and_view(self):
        url = reverse('items-of-an-item-category',kwargs={'item_category_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemListByItemCategoryAPIView)
    
    def test_items_of_a_lab_url_and_view(self):
        url = reverse('items-of-a-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, ItemListByLabAPIView)
    
    def test_temporary_handover_url_and_view(self):
        url = reverse('temporary-handover',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,TemporaryHandOverItemAPIView)
    
    def test_return_item_url_and_view(self):
        url = reverse('return-item',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,ReturnItemAPIView)
    
    def test_all_borrow_logs_url_and_view(self):
        url = reverse('all-borrow-logs')
        self.assertEqual(resolve(url).func.view_class,BorrowLogListAPIView)
    
    def test_all_borrow_logs_of_lab_url_and_view(self):
        url = reverse('all-borrow-logs-of-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,BorrowLogListofLabAPIView)
    
    def test_all_borrow_logs_of_student_url_and_view(self):
        url = reverse('all-borrow-logs-of-student',kwargs={'student_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,BorrowLogListofStudentAPIView)
    
    def test_currently_borrowed_from_lab_url_and_view(self):
        url = reverse('currently-borrowed-from-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,CurrentBorrowedItemListofLabAPIView)
    
    def test_currently_borrowed_by_student_url_and_view(self):
        url = reverse('currently-borrowed-by-student',kwargs={'student_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,CurrentBorrowedItemListofStudentAPIView)
    
    def test_item_handover_url_and_view(self):
        url = reverse('item-handover',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class,HandOverItemAPIView)