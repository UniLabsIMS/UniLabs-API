  

from django.contrib.auth.base_user import BaseUserManager
from custom_user.utils.email import Email
from custom_user.models import User
from custom_user.models import Role

# Admin manager to create admins
class AdminManager(BaseUserManager):
    def create_admin(self,email):
        admin=self.model(email=self.normalize_email(email),role=Role.ADMIN)
        password = self.make_random_password() # password is randomly generated when an admin is created
        print('Password>>>>>>>>>>>>>>>'+' '+password) #TODO: Remove this when email functionality done
        admin.set_password(password)
        
        try:
            Email.send_new_registration_email(email,Role.ADMIN,password)
        except:
            raise Exception('Error sending new registration email')
        admin.save()
        return admin

#Admin model which extends User model
class Admin(User):
    # add model fields specific to admin if any here

    objects = AdminManager()

    def __str__(self):
        return str(self.email)
