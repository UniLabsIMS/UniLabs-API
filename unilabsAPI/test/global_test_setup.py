from department.models import Department
from rest_framework.test import APITestCase
from faker import Faker
from custom_user.models import Role
from admin_user.models import Admin
from lab.models import Lab


class GlobalTestSetUp(APITestCase):

    def setUp(self):
        self.fake = Faker()

        # Admin for tests
        self.test_admin_user_data = {
            'email': 'test_admin1@gmail.com',
            'role': Role.ADMIN,
        }
        self.test_admin = Admin.objects.create_admin(email=self.test_admin_user_data['email'])


        # Department for test
        self.test_department_data = {
            'name': 'Test Department 1',
            'code': 'Test 1'
        }

        self.test_department = Department.objects.create(
            name=self.test_department_data["name"],
            code=self.test_department_data["code"]
        )

        # Lab for tests

        self.test_lab_data = {
            'name': 'Test Lab 1',
            'department': self.test_department
        }

        self.test_lab = Lab.objects.create(
            name=self.test_lab_data["name"],
            department=self.test_lab_data["department"]
        )


        return super().setUp()

    def tearDown(self):
        return super().tearDown()