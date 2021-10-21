from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import AdminRegisterAPIView,InitialSystemAdminRegiterAPIView,\
    SystemReportAPIView,AllAdminsAPIView


class TestUrls(SimpleTestCase):

    def test_admin_register_url_and_view(self):
        url = reverse('admin-register')
        self.assertEqual(resolve(url).func.view_class, AdminRegisterAPIView)

    def test_initial_admin_register_url_and_view(self):
        url = reverse('init-admin-register')
        self.assertEqual(resolve(url).func.view_class, InitialSystemAdminRegiterAPIView)

    def test_system_report_url_and_view(self):
        url = reverse('system-report')
        self.assertEqual(resolve(url).func.view_class, SystemReportAPIView)

    def test_get_all_admins_url_and_view(self):
        url = reverse('all-admins')
        self.assertEqual(resolve(url).func.view_class, AllAdminsAPIView)