from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from custom_user.models import Role, User
from department.models import Department
from custom_user.utils.default_passwords import DefaultPasswords
from custom_user.utils.email import Email
from decouple import config

# Admin Manager to create student
class StudentManager(BaseUserManager):
    def create_student(self, email, student_id, department):
        student=self.model(email=self.normalize_email(email),department=department, student_id=student_id,role= Role.STUDENT)
        password = DefaultPasswords.DEFAULT_DEBUG_STUDENT_PASSWORD if config('DEBUG') else self.make_random_password()
        print('Password>>>>>>>>>>>>>>>'+' '+password) #TODO: Remove this when email functionality done
        student.set_password(password)
        try:
            Email.send_new_registration_email(email,Role.STUDENT,password)
        except:
            raise Exception('Error sending new student registration email')
        student.save()
        return student

#Student model which extends User model
class Student(User):

    # add model fields specific to Student here
    student_id = models.CharField(unique=True,max_length=255)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = StudentManager()

    def __str__(self):
        return str(self.email)