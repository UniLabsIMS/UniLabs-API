from custom_user.utils.email import Email
from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from custom_user.utils.default_passwords import DefaultPasswords
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from custom_user.utils.utils import Util
from rest_framework import serializers
from .models import Role, User
from django.contrib import auth
from decouple import config
from django.contrib.auth import password_validation

# serializer class to handle login data
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3) # REQUIRED
    password = serializers.CharField(max_length=255, write_only=True) # REQUIRED
    token = serializers.SerializerMethodField()
    other_details = serializers.SerializerMethodField()
    user = None

    # set user variable by querying the db
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        try:
            self.user = User.objects.get(email=kwargs['data']['email'])
        except:
            pass

    # setting token serializer method field
    def get_token(self, obj):
        return self.user.token()

    # querying other role specific details
    def get_other_details(self, obj):
        return Util.get_role_specific_details(self.user)
        
    class Meta:
        model = User
        fields = ('id','token','email','password','role','first_name','last_name','contact_number','image','is_default_password','blocked','other_details',)
        read_only_fields = ('id','token','role','first_name','last_name','contact_number','image','is_default_password','blocked','other_details',)
       

    # Runs when .is_valid() is called and if possible authenticate the user
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if user.blocked:
            raise AuthenticationFailed('User blocked by admins')

        return user

# Refresh Auth Serializer 
class RefreshAuthSerializer(serializers.ModelSerializer):
    other_details = serializers.SerializerMethodField()
    user = None

    def __init__(self, *args, **kwargs):
        super(RefreshAuthSerializer, self).__init__(*args, **kwargs)
        try:
            self.user = kwargs['data']['user']
        except:
            pass

    # querying other role specific details
    def get_other_details(self, obj):
        return Util.get_role_specific_details(self.user)
    class Meta:
        model = User
        fields = ('id','email','role','first_name','last_name','contact_number','image','is_default_password','blocked','other_details',)
        read_only_fields = ('id','email', 'role','first_name','last_name','contact_number','image','is_default_password','blocked','other_details',)
    
    # Runs when .is_valid() is called and if possible authenticate the user
    def validate(self, attrs):
        if not self.user:
            raise AuthenticationFailed('Token Invalid')
        if self.user.blocked:
            raise AuthenticationFailed('User blocked by admins')
        return self.user

# Serializer to change user password
class ChangePasswordSerializer(serializers.Serializer):
    
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,min_length=8,max_length=31)

    class Meta:
        fields = ['current_password', 'new_password']
    
    def validate(self,data):
        try:
            password_validation.validate_password(data.get('new_password'))
        except ValidationError as exc:
            raise ValidationError(str(exc))
        return data

# Serializer to change user profile details
class UpdateProfileDetailsSerializer(serializers.ModelSerializer):
    contact_number = serializers.CharField(required=False,min_length=5,max_length=15)
    class Meta:
        model = User
        fields=("first_name","last_name","contact_number","image")

    def validate(self,attrs): #to makie sure contact number is only digits
        contact_number = attrs.get('contact_number',"")
        if contact_number !="" and (contact_number.isdigit()==False):
            raise ValidationError("Mobile Number Not Valid")  
        return attrs

# Serilizer to block request by admin user
class UserBlockUnblockSerializer(serializers.ModelSerializer):
    blocked = serializers.BooleanField(required=True)
    class Meta:
        model = User
        fields =['blocked',]
    
    def validate(self,data):
        if(self.instance.role == Role.ADMIN):
            raise ValidationError("Admins can not block/unblock other admins")
        return data

# Serilizer to handle forgot password
class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = User
        fields =['email',]
    
    def validate(self,data):
        if(not User.objects.filter(email=data.get('email')).exists()):
            raise ValidationError("Invalid email")
        return data

    @transaction.atomic
    def save(self,data):
        user = User.objects.get(email=data.get('email'))
        password = DefaultPasswords.DEFAULT_DEBUG_RESET_PASSWORD if (config('DEBUG','True')=='True') else BaseUserManager().make_random_password()
        user.set_password(password)
        if(not user.is_default_password):user.is_default_password=True
        user.save()
        try:
            Email.send_reset_password_email(data.get('email'),password)
        except Exception as e:
            raise Exception('Error sending reset password email')
