from rest_framework import serializers
from .models import LabAssistant
from lab.serializers import LabReadSerializer
from department.serializers import DepartmentReadSerializer

# Serializer to register a lab assistant
class LabAssistantRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= LabAssistant
        fields=["email","lab","department"]

    def create(self,validated_data):
        lab_assistant = LabAssistant.objects.create_lab_assistant(**validated_data,)
        return lab_assistant

# Lab Assistant specific data that should be returned as login reponse
class LabAssistantDetailSerializer(serializers.ModelSerializer):
    lab = LabReadSerializer()
    department = DepartmentReadSerializer()

    class Meta:
        model = LabAssistant
        fields=["lab","department"]