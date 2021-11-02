  

from custom_user.utils.default_passwords import DefaultPasswords
from decouple import config
from django.contrib.auth.base_user import BaseUserManager
from custom_user.utils.email import Email
from lab.models import Lab
from department.models import Department
from django.db import models
from custom_user.models import User
from custom_user.models import Role
from django.db import transaction
# Admin Manager to create lab assistant
class LabAssistantManager(BaseUserManager):
    @transaction.atomic
    def create_lab_assistant(self, email, lab, department):
        lab_assistant=self.model(email=self.normalize_email(email),lab=lab, department=department, role= Role.LAB_ASSISTANT)
        # TODO: password = DefaultPasswords.DEFAULT_DEBUG_LAB_ASSISTANT_PASSWORD if (config('DEBUG','True')=='True') else self.make_random_password()
        password = DefaultPasswords.DEFAULT_DEBUG_LAB_ASSISTANT_PASSWORD
        lab_assistant.set_password(password)
        lab_assistant.save()
        # try:
        #     Email.send_new_registration_email(email,Role.LAB_ASSISTANT,password)
        # except:
        #     raise Exception('Error sending new registration email')
        return lab_assistant

#Lab Assistant model which extends User model
class LabAssistant(User):

    # add model fields specific to Lab Assistant here
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = LabAssistantManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = 'lab_assistant_user'
