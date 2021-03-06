from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse

class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_display_item_url=reverse('new-display-item')
        cls.all_display_items_url=reverse('all-display-items')
        cls.single_display_item_url_name='single-display-item' # as we need path parameters
        cls.edit_display_item_url_name='update-display-item' # as we need path parameters
        cls.display_items_of_a_item_category_url_name = 'display-items-of-a-item-category'
        cls.display_items_of_a_lab_url_name='display-items-of-a-lab'
        cls.display_item_data={
            'name':'DISPLAY ITEM NAME',
            'item_category':cls.global_test_item_category.id,
            'description':'SAMPLE DESCRIPTION',
        }
        cls.display_item_edit_data={
            'name':'DISPLAY ITEM NAME EDITED',
            'description':'SAMPLE DESCRIPTION EDITED',
        }
        return

    def tearDown(self):
        return super().tearDown()