from rest_framework import serializers
from .models import LabAssistant
from lab.serializers import LabReadSerializer
from department.serializers import DepartmentReadSerializer

# Serializer to register a lab assistant
class LabAssistantRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= LabAssistant
        fields=["email","lab"]

    def create(self,validated_data):
        department = validated_data.get("lab").department
        lab_assistant = LabAssistant.objects.create_lab_assistant(**validated_data,department=department)
        return lab_assistant

# Lab Assistant specific data that should be returned as login reponse
class LabAssistantDetailSerializer(serializers.ModelSerializer):
    lab = LabReadSerializer()
    department = DepartmentReadSerializer()

    class Meta:
        model = LabAssistant
        fields=["lab","department"]

# Lab Assistant Details for Admins
class LabAssistantReadSerializer(serializers.ModelSerializer):
    lab = LabReadSerializer()
    department = DepartmentReadSerializer()

    class Meta:
        model = LabAssistant
        fields= ["id","email","first_name","last_name","contact_number","image","role","blocked","lab","department",]