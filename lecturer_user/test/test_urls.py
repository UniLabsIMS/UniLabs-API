from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LecturerRegisterAPIView,AllLecturersAPIView,LabLecturersAPIView


class TestUrls(SimpleTestCase):

    def test_lecturer_register_url_and_view(self):
        url = reverse('lecturer-register')
        self.assertEqual(resolve(url).func.view_class, LecturerRegisterAPIView)

    def test_all_lecturers_url_and_view(self):
        url = reverse('all-lecturers')
        self.assertEqual(resolve(url).func.view_class, AllLecturersAPIView)

    def test_lecturers_of_lab_url_and_view(self):
        url = reverse('lecturers-of-lab',kwargs={'lab_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, LabLecturersAPIView)