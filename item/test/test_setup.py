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
        cls.item_data={
            'display_item':cls.global_test_display_item_one.id,
        }
        cls.item={
            'display_item':cls.global_test_display_item_one,
        }

        return

    def tearDown(self):
        return super().tearDown()