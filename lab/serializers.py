from department.serializers import DepartmentReadSerializer
from .models import Lab
from rest_framework import serializers

#data visible as the response
class LabReadSerializer(serializers.ModelSerializer):
    department=DepartmentReadSerializer()
    class Meta:
        model = Lab
        fields="__all__"
    

#data for editing and creating lab
class LabWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields=('name','department','location','contact_no','contact_email',)

    # def validate(self,data):
    #     # To add department code infront of the given lab name
    #     try:
    #         department = Department.objects.get(id=data.get('department_id').id)
    #     except:
    #         raise serializers.ValidationError('An already existing department name is required')
    #     lab_name = data.get('name')
    #     data['name'] = department.code +' - ' + lab_name # example CSE - given lab name
    #     return data