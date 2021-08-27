from department.serializers import DepartmentReadSerializer
from .models import Lab
from rest_framework import serializers

#data visible as the response
class LabReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields="__all__"
class LabInDepthReadSerializer(serializers.ModelSerializer):
    department=DepartmentReadSerializer()
    class Meta:
        model = Lab
        fields="__all__"
    

#data for editing and creating lab
class LabWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields=('name','department','location','contact_no','contact_email',)
