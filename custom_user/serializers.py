from rest_framework.exceptions import AuthenticationFailed
from custom_user.utils.Utils import Util
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