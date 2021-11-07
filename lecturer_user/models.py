from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from custom_user.models import Role, User
from department.models import Department
from custom_user.utils.default_passwords import DefaultPasswords
from custom_user.utils.email import Email
from decouple import config
from lab.models import Lab
from uuid import uuid4
from django.db import transaction
from rest_framework.exceptions import ValidationError

# Admin Manager to create lecturer
class LecturerManager(BaseUserManager):
    @transaction.atomic
    def create_lecturer(self, email, lecturer_id, department, permitted_labs):
        lecturer=self.model(email=self.normalize_email(email),department=department, lecturer_id=lecturer_id,role= Role.LECTURER)
        password = DefaultPasswords.DEFAULT_DEBUG_LECTURER_PASSWORD if (config('DEBUG','True')=='True') else self.make_random_password()
        lecturer.set_password(password)
        lecturer.save()
        for lab_id in permitted_labs:
            if(LabLecturer.objects.filter(lab_id=lab_id,lecturer=lecturer).exists()):
                raise ValidationError({"permitted_labs":"Duplicate Lab"})
            LabLecturer.objects.create(lab_id=lab_id,lecturer=lecturer)
            
        try:
            Email.send_new_registration_email(email,Role.LECTURER,password)
        except:
            raise Exception('Error sending new lecturer registration email')
        return lecturer

# Lecturer model which extends User model
class Lecturer(User):
    # add model fields specific to Lecturer here
    lecturer_id = models.CharField(unique=True, max_length=255)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = LecturerManager()

    class Meta:
        db_table = 'lecturer'

    def __str__(self):
        return str(self.email)

# LabLecturer model to indicate relationship between lecturers and labs
class LabLecturer(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab,on_delete=models.CASCADE)

    class Meta:
        db_table = 'lab_lecturer'
        unique_together = (('lecturer', 'lab'),)
