from unilabsAPI.test.global_test_setup import GlobalTestSetUp
from django.urls import reverse 


class TestSetUp(GlobalTestSetUp):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.new_item_category_url=reverse('item_category-create')
        cls.all_item_categories_url=reverse('all_item_categories')
        cls.single_item_category_url_name='single-item_category' # as we need path parameters
        cls.item_category_data={
            'name':'TEST ITEM_CATEGORY NAME',
            'lab':cls.global_test_lab.id,
            'description':'SAMPLE DESCRIPTION',
        }
        return

    def tearDown(self):
        return super().tearDown()