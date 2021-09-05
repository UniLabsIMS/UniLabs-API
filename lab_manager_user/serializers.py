from rest_framework import serializers
from .models import LabManager
from lab.serializers import LabReadSerializer
from department.serializers import DepartmentReadSerializer

# Serializer to register a lab manager
class LabManagerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= LabManager
        fields=["email","lab"]

    def create(self,validated_data):
        department = validated_data.get('lab').department
        lab_manager = LabManager.objects.create_lab_manager(**validated_data,department=department)
        return lab_manager

# Lab Manager specific data that should be returned as login reponse
class LabManagerDetailSerializer(serializers.ModelSerializer):
    lab = LabReadSerializer()
    department = DepartmentReadSerializer()

    class Meta:
        model = LabManager
        fields=["lab","department"]


# Lab Manager Details for Admins
class LabManagerReadSerializer(serializers.ModelSerializer):
    lab = LabReadSerializer()
    department = DepartmentReadSerializer()

    class Meta:
        model = LabManager
        fields= ["email","first_name","last_name","contact_number","image","role","lab","department",]