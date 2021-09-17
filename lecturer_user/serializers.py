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
        for lab_id in labs:
            if(not Lab.objects.filter(id=lab_id).exists()):
                raise ValidationError("Invalid lab id")
        return data

    def create(self,validated_data):
        lecturer = Lecturer.objects.create_lecturer(**validated_data)
        return lecturer