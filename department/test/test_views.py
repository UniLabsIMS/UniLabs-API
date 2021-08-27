
from .test_setup import TestSetUp

class TestViews(TestSetUp):
    def test_unauthenticated_user_cannot_get_departments(self):
        res = self.client.get(self.all_departments_url,format='json')
        self.assertEqual(res.status_code, 401)

    def test_authnaticated_user_can_get_departments(self):
        self.client.force_authenticate(user=self.test_admin)
        res = self.client.get(self.all_departments_url,format='json')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data),0)

    def test_authenticated_admin_can_create_departments(self):
        self.client.force_authenticate(user=self.test_admin)
        res = self.client.post(self.new_department_url,self.department_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone('id')
