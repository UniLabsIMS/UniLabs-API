from rest_framework import serializers
from .models import LabManager


# Serializer to register a lab manager
class LabManagerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= LabManager
        fields=["email","lab","department"]

    def create(self,validated_data):
        lab_manager = LabManager.objects.create_lab_manager(**validated_data,)
        return lab_manager

# Lab Manager specific data that should be returned as login reponse
class LabManagerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabManager
        exclude = "__all__"