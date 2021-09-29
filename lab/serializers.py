from django.db import transaction
from rest_framework.exceptions import ValidationError
from lecturer_user.models import LabLecturer, Lecturer
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
    assigened_lecturers = serializers.SerializerMethodField()

    def get_assigened_lecturers(self,obj):
        lab_lecs = LabLecturer.objects.filter(lab=obj)
        lecturers = []
        for lab_lec_obj in lab_lecs:
            from lecturer_user.serializers import LecturerSummarizedReadSerializer
            lecturers.append(LecturerSummarizedReadSerializer(lab_lec_obj.lecturer).data)
        return lecturers
    class Meta:
        model = Lab
        fields=["id","name","location","department","location","contact_no","contact_email","image","created_at","assigened_lecturers"]
    

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

# Serializer to assign lecturers to lab
class LabAssignLecturerSerializer(serializers.ModelSerializer):
    lecturers = serializers.ListField(write_only=True)
    class Meta:
        model= LabLecturer
        fields=["lab","lecturers"]

    def validate(self,data):
        lecturers = data.get('lecturers')
        lab = data.get('lab')
        for lecturer_id in lecturers:
            try:
                lecturer = Lecturer.objects.get(id=lecturer_id)
            except:
                raise ValidationError("Lecturer ID invalid")
            if(LabLecturer.objects.filter(lab=lab,lecturer=lecturer).exists()):
                raise ValidationError("Lecturer Already Assigned to Lab")
            if(lab.department!=lecturer.department):
                raise ValidationError("Lab can have only lecturers from its department")
        
        return data

    @transaction.atomic
    def save(self,validated_data):
        lecturers = validated_data.get('lecturers')
        lab_id = validated_data.get('lab')
        for lecturer_id in lecturers:
            LabLecturer.objects.create(lab_id=lab_id,lecturer_id=lecturer_id)
        return