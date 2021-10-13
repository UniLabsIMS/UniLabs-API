from django.db import transaction
from rest_framework.exceptions import ValidationError
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



'''
In the serializer
Not the model serializer we use, we use serialozers.Serializer 

You need to have several method fields which are read only (ex: total_item_count, bo_itm_count,.....)


'''
class LabReportReadSerializer(serializers.Serializer):
    lab_id = serializers.CharField(write_only=True)
    total_item_count = serializers.SerializerMethodField(read_only=True)
    currently_borrowed_items_count=serializers.SerializerMethodField(read_only=True)
    percentage_of_borrowed_items_currently=serializers.SerializerMethodField(read_only=True)
    damaged_items_count=serializers.SerializerMethodField(read_only=True)
    percentage_of_damaged_items=serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        lab_id=data.get('lab_id')
        try:
            lab=Lab.objects.get(id=lab_id)
        except:
            raise ValidationError('Lab id should be valid id')

        return data
    
    def get_total_item_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        total_item_count = Item.objects.filter(lab_id=self.lab_id).count()
        self.total_item_count=total_item_count
        return total_item_count
    
    def get_currently_borrowed_items_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        currently_borrowed_items_count = Item.objects.filter(lab_id=self.lab_id,state=State.BORROWED).count()
        self.currently_borrowed_items_count=currently_borrowed_items_count
        return currently_borrowed_items_count
    
    def get_percentage_of_borrowed_items_currently(self,validated_data):
        percentage_of_borrowed_items_currently = round(self.currently_borrowed_items_count/self.total_item_count,2)*100
        self.percentage_of_borrowed_items_currently=percentage_of_borrowed_items_currently
        return percentage_of_borrowed_items_currently
    
    def get_damaged_items_count(self,validated_data):
        self.lab_id=validated_data.get('lab_id')
        damaged_items_count = Item.objects.filter(lab_id=self.lab_id,state=State.DAMAGED).count()
        self.damaged_items_count=damaged_items_count
        return damaged_items_count
    
    def get_percentage_of_damaged_items(self,validated_data):
        percentage_of_damaged_items = round(self.damaged_items_count/self.total_item_count,2)*100
        self.percentage_of_damaged_items=percentage_of_damaged_items
        return percentage_of_damaged_items
    

