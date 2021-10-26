from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import DepartmentListAPIView,DepartmentCreateAPIView,DepartmentRetrieveAPIView,DepartmentUpdateAPIView


class TestUrls(SimpleTestCase):

    def test_all_departments_url_and_view(self):
        url = reverse('all-departments')
        self.assertEqual(resolve(url).func.view_class, DepartmentListAPIView)

    def test_single_department_url_and_view(self):
        url = reverse('single-department',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, DepartmentRetrieveAPIView)
    
    def test_department_create_url_and_view(self):
        url = reverse('department-create')
        self.assertEqual(resolve(url).func.view_class, DepartmentCreateAPIView)
    
    def test_department_update_url_and_view(self):
        url = reverse('department-update',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, DepartmentUpdateAPIView)