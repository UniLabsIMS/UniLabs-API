from lab_manager_user.models import LabManager
from department.models import Department
from rest_framework.test import APITestCase
from faker import Faker
from custom_user.models import Role
from admin_user.models import Admin
from lab.models import Lab


class GlobalTestSetUp(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()

        # Admin for tests
        cls.global_test_admin_user_data = {
            'email': 'test_admin1@gmail.com',
            'role': Role.ADMIN,
        }
        cls.global_test_admin = Admin.objects.create_admin(email=cls.global_test_admin_user_data['email'])


        # Department for test
        cls.global_test_department_data = {
            'name': 'Test Department 1',
            'code': 'TestDepCode1'
        }

        cls.global_test_department = Department.objects.create(
            name=cls.global_test_department_data["name"],
            code=cls.global_test_department_data["code"]
        )

        # Labs for tests

        cls.global_test_lab_data = {
            'name': 'Test Lab 1',
            'department': cls.global_test_department
        }

        cls.global_test_lab = Lab.objects.create(
            name=cls.global_test_lab_data["name"],
            department=cls.global_test_lab_data["department"]
        )

        # Lab Managers for tests

        cls.global_test_lab_manager_data = {
            'email': cls.fake.email(),
            'lab': cls.global_test_lab,
            'department': cls.global_test_department
        }

        cls.global_test_lab_manager = LabManager.objects.create_lab_manager(
            email = cls.global_test_lab_manager_data["email"],
            lab = cls.global_test_lab_manager_data["lab"],
            department = cls.global_test_lab_manager_data["department"]
        )


        return

    def tearDown(self):
        return super().tearDown()