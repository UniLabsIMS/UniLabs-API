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
    LAB_STAFF = 'Lab_Staff', _('Lab_Staff')
    LECTURER = 'Lecturer', _('Lecturer')
    STUDENT = 'Student', _('Student')

# UserManager class to manage user creation
class UserManager(BaseUserManager):
    def create_user(self,email,role):
        if email is None:
            raise TypeError('Users should have an email')
        if role is None:
            raise TypeError('Users should have a role')
            
        user=self.model(email=self.normalize_email(email))
        password = self.make_random_password() # password is randomly generated when a user is created
        print('Password>>>>>>>>>>>>>>>'+' '+password) #TODO: Remove this when email functionality done
        user.set_password(password)
        user.role=role
        try:
            Email.send_new_registration_email(email,role,password)
        except:
            raise Exception('Error sending new registration email')
        user.save()
        return user

    def create_superuser(self,username,email,role=Role.ADMIN):
        user = self.create_user(username,email,role)
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