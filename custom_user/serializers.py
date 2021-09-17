from rest_framework.exceptions import AuthenticationFailed, ValidationError
from custom_user.utils.utils import Util
from rest_framework import serializers
from .models import User
from django.contrib import auth

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
        fields = ('token','email','password','role','first_name','last_name','contact_number','image','is_default_password','other_details',)
        read_only_fields = ('token','role','first_name','last_name','contact_number','image','is_default_password','other_details',)
       

    # Runs when .is_valid() is called and if possible authenticate the user
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

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
        fields = ('email','role','first_name','last_name','contact_number','image','is_default_password','other_details',)
        read_only_fields = ('email', 'role','first_name','last_name','contact_number','image','is_default_password','other_details',)
    
    # Runs when .is_valid() is called and if possible authenticate the user
    def validate(self, attrs):
        if not self.user:
            raise AuthenticationFailed('Token Invalid')
        return self.user

# Serializer to change user password
class ChangePasswordSerializer(serializers.Serializer):
    
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,min_length=6,max_length=31)

    class Meta:
        fields = ['current_password', 'new_password']

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