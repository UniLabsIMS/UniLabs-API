from lab.serializers import LabReadSerializer
from department.serializers import DepartmentReadSerializer
from rest_framework import serializers
from .models import LabLecturer, Lecturer
from lab.models import Lab
from rest_framework.exceptions import ValidationError

# Serializer to register a lecturer
class LecturerRegisterSerializer(serializers.ModelSerializer):
    permitted_labs = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model= Lecturer
        fields=["email","lecturer_id","department","permitted_labs"]

    def validate(self,data):
        labs = data.get('permitted_labs')
        department = data.get('department')
        for lab_id in labs:
            lab = Lab.objects.filter(id=lab_id)
            if(lab.count()==0):
                raise ValidationError("Invalid lab id")
            if(lab[0].department!=department):
                raise ValidationError("all the labs must be under the declared deparment")
        return data

    def create(self,validated_data):
        lecturer = Lecturer.objects.create_lecturer(**validated_data)
        return lecturer

# Lecturer specific data that should be returned as login reponse
class LecturerDetailSerializer(serializers.ModelSerializer):
    department = DepartmentReadSerializer()
    permitted_labs = serializers.SerializerMethodField()

    def get_permitted_labs(self,obj):
        lab_lecs = LabLecturer.objects.filter(lecturer=obj)
        labs = []
        for lab_lec_obj in lab_lecs:
            labs.append(LabReadSerializer(lab_lec_obj.lab).data)
        return labs
    class Meta:
        model = Lecturer
        fields=["lecturer_id","department","permitted_labs"]

# Lecturer Details for Admins
class LecturerReadSerializer(serializers.ModelSerializer):
    department = DepartmentReadSerializer()
    permitted_labs = serializers.SerializerMethodField()

    def get_permitted_labs(self,obj):
        lab_lecs = LabLecturer.objects.filter(lecturer=obj)
        labs = []
        for lab_lec_obj in lab_lecs:
            labs.append(LabReadSerializer(lab_lec_obj.lab).data)
        return labs
    class Meta:
        model = Lecturer
        fields= ["id","lecturer_id","email","first_name","last_name","contact_number","image","role","blocked","department","permitted_labs"]