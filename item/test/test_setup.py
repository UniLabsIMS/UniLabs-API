from item.models import State
from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse

class TestSetup(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_item_url=reverse('new-item')
        cls.all_items_url=reverse('all-items')
        cls.single_item_url_name='single-item' # as we need path parameters
        cls.items_of_a_display_item_url_name = 'items-of-a-display-item'
        cls.delete_item_url_name = 'delete-item'
        cls.items_of_an_item_category_url_name='items-of-an-item-category'
        cls.items_of_a_lab_url_name='items-of-a-lab'
        cls.temporary_handover_url_name='temporary-handover'
        cls.edit_item_url_name='update-item'
        cls.item_data={
            'display_item':cls.global_test_display_item_one.id,
        }
        cls.item={
            'display_item':cls.global_test_display_item_one,
        }
        cls.student_data={
            'student_uuid':cls.global_test_student.id,
        }
        cls.edit_item_data={
            'state':State.BORROWED,
        }

        return

    def tearDown(self):
        return super().tearDown()