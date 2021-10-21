from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LabManagerRegisterAPIView,AllLabManagersAPIView


class TestUrls(SimpleTestCase):

    def test_lab_manager_register_url_and_view(self):
        url = reverse('lab-manager-register')
        self.assertEqual(resolve(url).func.view_class, LabManagerRegisterAPIView)

    def test_all_lab_managers_url_and_view(self):
        url = reverse('all-lab-managers')
        self.assertEqual(resolve(url).func.view_class, AllLabManagersAPIView)
