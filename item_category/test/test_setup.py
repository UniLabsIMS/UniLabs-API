from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse 


class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_item_category_url=reverse('new-item-category')
        cls.all_item_categories_url=reverse('all-item-categories')
        cls.single_item_category_url_name='single-item-category' # as we need path parameters
        cls.edit_item_category_url_name='update-item-category' # as we need path parameters
        cls.item_categories_of_a_lab_url_name = 'item-categories-of-a-lab'
        cls.item_category_data={
            'name':'ITEM CATEGORY NAME',
            'lab':cls.global_test_lab.id,
            'description':'SAMPLE DESCRIPTION',
        }
        cls.item_category_edit_data={
            'name':'ITEM CATEGORY NAME EDITED',
            'description':'SAMPLE DESCRIPTION EDITED',
        }
        return

    def tearDown(self):
        return super().tearDown()