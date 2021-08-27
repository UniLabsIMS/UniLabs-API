from .test_setup import TestSetUp

class TestViews(TestSetUp):

    def test_authenticated_admin_can_create_labs(self):
        self.client.force_authenticate(user=self.test_admin)
        res = self.client.post(self.new_lab_url,self.lab_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIsNotNone('id')

    def test_lab_creation_must_fail_if_department_id_is_invalid(self):
        self.client.force_authenticate(user=self.test_admin)
        data = self.lab_data.copy()
        data['department'] = '123' # Invalid department id
        res = self.client.post(self.new_lab_url,data,format="json")
        self.assertEqual(res.status_code, 400)