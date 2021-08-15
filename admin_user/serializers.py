from rest_framework import serializers
from .models import Admin


# Serializer to register an admin
class AdminRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= Admin
        fields=["email"]

    def create(self,validated_data):
        admin = Admin.objects.create_admin(**validated_data,)
        return admin

# Admin specific data that should be returned as login reponse
class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = "__all__"