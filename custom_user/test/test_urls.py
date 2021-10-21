from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import UserLoginAPIView,ChangePasswordAPIView,\
UpdateProfileDetialsAPIView,RefreshUserAuthAPIView,\
    BlockUnblockAPIView,ResetPasswordAPIView


class TestUrls(SimpleTestCase):

    def test_login_url_and_view(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, UserLoginAPIView)

    def test_change_pw_url_and_view(self):
        url = reverse('change-password')
        self.assertEqual(resolve(url).func.view_class, ChangePasswordAPIView)

    def test_profile_update_url_and_view(self):
        url = reverse('update-profile')
        self.assertEqual(resolve(url).func.view_class, UpdateProfileDetialsAPIView)

    def test_refresh_auth_url_and_view(self):
        url = reverse('refresh-auth')
        self.assertEqual(resolve(url).func.view_class, RefreshUserAuthAPIView)

    def test_user_block_unblock_url_and_view(self):
        url = reverse('user-block',kwargs={'id': '539da720-f58f-49a9-9e44-b8dacb4e681f'})
        self.assertEqual(resolve(url).func.view_class, BlockUnblockAPIView)

    def test_reset_password_url_and_view(self):
        url = reverse('reset-password')
        self.assertEqual(resolve(url).func.view_class, ResetPasswordAPIView)