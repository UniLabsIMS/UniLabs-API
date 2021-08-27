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
        cls.test_admin_user_data = {
            'email': 'test_admin1@gmail.com',
            'role': Role.ADMIN,
        }
        cls.test_admin = Admin.objects.create_admin(email=cls.test_admin_user_data['email'])


        # Department for test
        cls.test_department_data = {
            'name': 'Test Department 1',
            'code': 'Test 1'
        }

        cls.test_department = Department.objects.create(
            name=cls.test_department_data["name"],
            code=cls.test_department_data["code"]
        )

        # Lab for tests

        cls.test_lab_data = {
            'name': 'Test Lab 1',
            'department': cls.test_department
        }

        cls.test_lab = Lab.objects.create(
            name=cls.test_lab_data["name"],
            department=cls.test_lab_data["department"]
        )


        return

    def tearDown(self):
        return super().tearDown()