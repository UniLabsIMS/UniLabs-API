from rest_framework import serializers
from .models import Student
from lab.serializers import LabReadSerializer
from department.serializers import DepartmentReadSerializer

# Serializer to register a student
class StudentRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= Student
        fields=["email","student_id","department"]

    def create(self,validated_data):
        student = Student.objects.create_student(**validated_data)
        return student

# Student specific data that should be returned as login reponse
class StudentDetailSerializer(serializers.ModelSerializer):
    department = DepartmentReadSerializer()

    class Meta:
        model = Student
        fields=["student_id","department"]


# Student Details for Admins
class StudentReadSerializer(serializers.ModelSerializer):
    department = DepartmentReadSerializer()

    class Meta:
        model = Student
        fields= ["id","student_id","email","first_name","last_name","contact_number","image","role","department",]