from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LabAssistantRegisterAPIView,AllLabAssistantsAPIView


class TestUrls(SimpleTestCase):

    def test_lab_assistant_register_url_and_view(self):
        url = reverse('lab-assistant-register')
        self.assertEqual(resolve(url).func.view_class, LabAssistantRegisterAPIView)

    def test_all_lab_assistants_url_and_view(self):
        url = reverse('all-lab-assistants')
        self.assertEqual(resolve(url).func.view_class, AllLabAssistantsAPIView)
