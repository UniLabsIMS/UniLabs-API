from django.db import transaction
from rest_framework.exceptions import ValidationError
from display_item.models import DisplayItem
from item_category.models import ItemCategory
from lab_assistant_user.models import LabAssistant
from lab_manager_user.models import LabManager
from lecturer_user.models import LabLecturer, Lecturer
from department.serializers import DepartmentReadSerializer
from .models import Lab
from rest_framework import serializers
from item.models import Item, State

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
        fields=('id','name','department','location','contact_no','contact_email','image')# id wont show up as required, as editable is set to false

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
        lab = validated_data.get('lab')
        for lecturer_id in lecturers:
            LabLecturer.objects.create(lab=lab,lecturer_id=lecturer_id)
        return

# lab report
class LabReportReadSerializer(serializers.Serializer):
    lab_id = serializers.CharField(write_only=True)
    total_category_count=serializers.SerializerMethodField(read_only=True)
    total_display_item_count=serializers.SerializerMethodField(read_only=True)
    total_item_count = serializers.SerializerMethodField(read_only=True)
    available_item_count = serializers.SerializerMethodField(read_only=True)
    borrowed_item_count=serializers.SerializerMethodField(read_only=True)
    temp_borrowed_item_count=serializers.SerializerMethodField(read_only=True)
    damaged_item_count=serializers.SerializerMethodField(read_only=True)
    lab_manager_count=serializers.SerializerMethodField(read_only=True)
    lab_assistant_count = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        lab_id=data.get('lab_id')
        try:
            lab=Lab.objects.get(id=lab_id)
        except:
            raise ValidationError('Lab id should be valid id')

        return data
    
    def get_total_category_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        total_category_count = ItemCategory.objects.filter(lab_id=self.lab_id).count()
        self.total_category_count=total_category_count
        return total_category_count

    def get_total_display_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        total_display_item_count = DisplayItem.objects.filter(lab_id=self.lab_id).count()
        self.total_display_item_count=total_display_item_count
        return total_display_item_count

    def get_total_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        total_item_count = Item.objects.filter(lab_id=self.lab_id).count()
        self.total_item_count=total_item_count
        return total_item_count

    def get_available_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        available_item_count = Item.objects.filter(lab_id=self.lab_id,state=State.AVAILABLE).count()
        self.available_item_count=available_item_count
        return available_item_count
    
    def get_borrowed_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        borrowed_item_count = Item.objects.filter(lab_id=self.lab_id,state=State.BORROWED).count()
        self.borrowed_item_count=borrowed_item_count
        return borrowed_item_count
    
    def get_temp_borrowed_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        temp_borrowed_item_count = Item.objects.filter(lab_id=self.lab_id,state=State.TEMP_BORROWED).count()
        self.temp_borrowed_item_count=temp_borrowed_item_count
        return temp_borrowed_item_count
    
    def get_damaged_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        damaged_item_count = Item.objects.filter(lab_id=self.lab_id,state=State.DAMAGED).count()
        self.damaged_item_count=damaged_item_count
        return damaged_item_count
    
    def get_lab_manager_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        lab_manager_count = LabManager.objects.filter(lab_id=self.lab_id).count()
        self.lab_manager_count=lab_manager_count
        return lab_manager_count
    
    def get_lab_assistant_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        lab_assistant_count = LabAssistant.objects.filter(lab_id=self.lab_id).count()
        self.lab_assistant_count=lab_assistant_count
        return lab_assistant_count
    

            