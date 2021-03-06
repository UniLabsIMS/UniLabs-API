from custom_user.utils.default_passwords import DefaultPasswords
from django.contrib.auth.base_user import BaseUserManager
from custom_user.utils.email import Email
from custom_user.models import User
from custom_user.models import Role
from decouple import config
from django.db import transaction
# Admin manager to create admins
class AdminManager(BaseUserManager):
    @transaction.atomic
    def create_admin(self,email):
        admin=self.model(email=self.normalize_email(email),role=Role.ADMIN)
        password = DefaultPasswords.DEFAULT_DEBUG_ADMIN_PASSWORD if (config('DEBUG','True')=='True') else self.make_random_password() # password is randomly generated when an admin is created
        admin.set_password(password)
        admin.save()
        try:
            Email.send_new_registration_email(email,Role.ADMIN,password)
        except Exception as e:
            raise Exception('Error sending new registration email')
        return admin

#Admin model which extends User model
class Admin(User):
    # add model fields specific to admin if any here

    objects = AdminManager()

    def __str__(self):
        return str(self.email)
    
    class Meta:
        db_table = 'admin_user'
