from .models import Department
from rest_framework import serializers,viewsets

#data visible as the response
class DepartmentReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields='__all__'

#data for editing and creating department
class DepartmentWriteSerializer(serializers.ModelSerializer):
    name=serializers.CharField(max_length=255)

    class Meta:
        model = Department
        fields=('name',)