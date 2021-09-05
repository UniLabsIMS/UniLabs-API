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
    

#data for creating lab
class LabWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields=('id','name','department','location','contact_no','contact_email',)# id wont show up as required, as editable is set to false

#data for editing and creating lab
class LabUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields=('id','name','location','contact_no','contact_email',) #department id is not editable