from custom_user.utils.email import Email
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from knox.models import AuthToken
from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

# Role Field options
class Role(models.TextChoices):
    ADMIN = 'Admin', _('Admin')
    LAB_MANAGER = 'Lab_Manager', _('Lab_Manager')
    LAB_ASSISTANT = 'Lab_Assistant', _('Lab_Assistant')
    LECTURER = 'Lecturer', _('Lecturer')
    STUDENT = 'Student', _('Student')

# UserManager class to manage django superuser creation
class UserManager(BaseUserManager):

    def create_superuser(self,email,role=Role.ADMIN):
        user = self.model(email,role)
        user.save()
        return user



# Custom user class which extends django user class
class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(default=uuid4, primary_key=True,editable=False)
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    role =  models.CharField(max_length=31, choices=Role.choices)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    contact_number = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='users/',blank=True) 
    is_default_password = models.BooleanField(default=True) # whether the account has the default password given at registration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"

    objects=UserManager()

    def __str__(self):
        return self.email

    def token(self):
        token = AuthToken.objects.create(self)[1]
        return str(token)
    
    class Meta:
        db_table = 'custom_user'
