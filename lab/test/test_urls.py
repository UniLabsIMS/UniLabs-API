from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .. import views

class TestUrls(SimpleTestCase):

    def test_all_labs_url_and_view(self):
        url = reverse('all-labs')
        self.assertEqual(resolve(url).func.view_class, views.LabListAPIView)

    def test_single_lab_url_and_view(self):
        url = reverse('single-lab',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, views.LabRetrieveAPIView)
    
    def test_lab_create_url_and_view(self):
        url = reverse('lab-create')
        self.assertEqual(resolve(url).func.view_class, views.LabCreateAPIView)
    
    def test_lab_update_url_and_view(self):
        url = reverse('lab-update',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, views.LabUpdateAPIView)
    
    def test_labs_of_a_department_url_and_view(self):
        url = reverse('labs-of-a-department',kwargs={'department_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, views.LabListByDepartmentAPIView)
    
    def test_assign_lectures_url_and_view(self):
        url = reverse('assign-lecturers')
        self.assertEqual(resolve(url).func.view_class, views.LabAssignLecturerAPIView)
    
    def test_lab_report_url_and_view(self):
        url = reverse('lab-report',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, views.LabReportAPIView)