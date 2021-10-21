from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import StudentRegisterAPIView,AllStudentsAPIView,SingleStudentAPIView


class TestUrls(SimpleTestCase):

    def test_student_register_url_and_view(self):
        url = reverse('student-register')
        self.assertEqual(resolve(url).func.view_class, StudentRegisterAPIView)

    def test_all_students_url_and_view(self):
        url = reverse('all-students')
        self.assertEqual(resolve(url).func.view_class, AllStudentsAPIView)

    def test_get_student_url_and_view(self):
        url = reverse('get-student',kwargs={'student_id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, SingleStudentAPIView)