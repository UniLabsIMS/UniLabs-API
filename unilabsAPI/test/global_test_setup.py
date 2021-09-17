from lecturer_user.models import Lecturer
from display_item.models import DisplayItem
from item_category.models import ItemCategory
from lab_manager_user.models import LabManager
from lab_assistant_user.models import LabAssistant
from department.models import Department
from student_user.models import Student
from rest_framework.test import APITestCase
from faker import Faker
from admin_user.models import Admin
from lab.models import Lab
from item.models import Item


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

        cls.global_test_lab_two = Lab.objects.create(
            name='Test Lab 2',
            department=cls.global_test_department
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


        # Item Categories for tests
        cls.global_test_item_category=ItemCategory.objects.create(
            name='Test Item Category 1',
            lab=cls.global_test_lab
        )

        cls.global_test_item_category_two=ItemCategory.objects.create(
            name='Test Item Category 2',
            lab=cls.global_test_lab_two
        )

        cls.global_test_item_category_three=ItemCategory.objects.create(
            name='Test Item Category 3',
            lab=cls.global_test_lab
        )

        # Display Items for tests
        cls.global_test_display_item_one=DisplayItem.objects.create(
            name='Test Display Item 1',
            item_category=cls.global_test_item_category,
            lab=cls.global_test_lab,
            item_count=0,
        )

        cls.global_test_display_item_two=DisplayItem.objects.create(
            name='Test Display Item 2',
            item_category=cls.global_test_item_category_two,
            lab=cls.global_test_lab_two,
            item_count=0,
        )

        cls.global_test_display_item_three=DisplayItem.objects.create(
            name='Test Display Item 3',
            item_category=cls.global_test_item_category_three,
            lab=cls.global_test_lab,
            item_count=0,
        )

        #Items for test

        cls.global_test_item_one=Item.objects.create(
            display_item=cls.global_test_display_item_one,
            item_category=cls.global_test_item_category,
            lab=cls.global_test_lab
        )

        cls.global_test_item_two=Item.objects.create(
            display_item=cls.global_test_display_item_two,
            item_category=cls.global_test_item_category_two,
            lab=cls.global_test_lab_two
        )

        cls.global_test_item_three=Item.objects.create(
            display_item=cls.global_test_display_item_three,
            item_category=cls.global_test_item_category_three,
            lab=cls.global_test_lab
        )

         # Student for tests
        cls.global_test_student = Student.objects.create_student(
            email = cls.fake.email(),
            student_id = "123321X",
            department = cls.global_test_department
        )

        # Lecturer for tests
        cls.global_test_lecturer = Lecturer.objects.create_lecturer(
            email = cls.fake.email(),
            lecturer_id = "1433T1X",
            department = cls.global_test_department,
            permitted_labs = [cls.global_test_lab.id,]
        )


        return

    def tearDown(self):
        return super().tearDown()