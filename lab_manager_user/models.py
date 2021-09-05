from custom_user.utils.default_passwords import DefaultPasswords
from decouple import config
from django.contrib.auth.base_user import BaseUserManager
from custom_user.utils.email import Email
from lab.models import Lab
from department.models import Department
from django.db import models
from custom_user.models import User
from custom_user.models import Role

# Admin manager to create lab managers
class LabManagerUserManager(BaseUserManager):
    def create_lab_manager(self, email, lab, department):
        lab_manager=self.model(email=self.normalize_email(email),lab=lab, department=department, role= Role.LAB_MANAGER)
        password = DefaultPasswords.DEFAULT_DEBUG_LAB_MANAGER_PASSWORD if (config('DEBUG','True')=='True') else self.make_random_password()
        print('Password>>>>>>>>>>>>>>>'+' '+password) #TODO: Remove this when email functionality done
        lab_manager.set_password(password)
        try:
            Email.send_new_registration_email(email,Role.LAB_MANAGER,password)
        except:
            raise Exception('Error sending new registration email')
        lab_manager.save()
        return lab_manager

#Lab Manager model which extends User model
class LabManager(User):

    # add model fields specific to Lab Manager here
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = LabManagerUserManager()

    def __str__(self):
        return str(self.email)
