from datetime import timedelta
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from knox.models import AuthToken
from django.db import models
from django.utils.translation import gettext_lazy as _


# Role Field options
class Role(models.TextChoices):
    ADMIN = 'Admin', _('Admin')
    LAB_MANAGER = 'Lab_Manager', _('Lab_Manager')
    LAB_STAFF = 'Lab_Staff', _('Lab_Staff')
    LECTURER = 'Lecturer', _('Lecturer')
    STUDENT = 'Student', _('Student')

# UserManager class to manage user creation
class UserManager(BaseUserManager):
    def create_user(self,email,role):
        if email is None:
            raise TypeError('Users should have an email')
        user=self.model(email=self.normalize_email(email))
        password = self.make_random_password() # password is randomly generated when a user is created
        user.set_password(password)
        user.role=role
        user.save()
        # add email functionality here
        return user

    def create_superuser(self,username,email,role=Role.ADMIN):
        user = self.create_user(username,email,role)
        user.save()
        return user



# Custom user class which extends django user class
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    role =  models.CharField(max_length=31, choices=Role.choices)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    contact_number = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='users/',blank=True) 
    is_default_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"

    objects=UserManager()

    def __str__(self):
        return self.email

    def user_token(self):
        token = AuthToken.objects.create(self)[1]
        return str(token)