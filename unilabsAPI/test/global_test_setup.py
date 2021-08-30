from item_category.models import Item_Category
from lab_manager_user.models import LabManager
from lab_assistant_user.models import LabAssistant
from department.models import Department
from rest_framework.test import APITestCase
from faker import Faker
from admin_user.models import Admin
from lab.models import Lab


class GlobalTestSetUp(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()

        # Admin for tests
        cls.global_test_admin = Admin.objects.create_admin(
            email='test_admin1@gmail.com'
        )


        # Department for test
        cls.global_test_department = Department.objects.create(
            name='Test Department 1',
            code='TestDepCode1',
        )

        # Labs for tests
        cls.global_test_lab = Lab.objects.create(
            name='Test Lab 1',
            department=cls.global_test_department
        )

        # Item_Category for tests
        cls.global_test_item_category=Item_Category.objects.create(
            name='Test Item_Category 1',
            lab=cls.global_test_lab
        )

        # Lab Managers for tests
        cls.global_test_lab_manager = LabManager.objects.create_lab_manager(
            email = cls.fake.email(),
            lab = cls.global_test_lab,
            department = cls.global_test_department
        )

        # Lab Assistant for tests
        cls.global_test_lab_assistant = LabAssistant.objects.create_lab_assistant(
            email = cls.fake.email(),
            lab = cls.global_test_lab,
            department = cls.global_test_department
        )


        return

    def tearDown(self):
        return super().tearDown()