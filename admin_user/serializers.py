from rest_framework import serializers
from department.models import Department

from lab.models import Lab
from .models import Admin
from display_item.models import DisplayItem
from item_category.models import ItemCategory
from item.models import Item, State
from admin_user.models import Admin
from student_user.models import Student
from lab_manager_user.models import LabManager
from lab_assistant_user.models import LabAssistant
from lecturer_user.models import Lecturer
from custom_user.models import User
# Serializer to register an admin
class AdminRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model= Admin
        fields=["email"]

    def create(self,validated_data):
        admin = Admin.objects.create_admin(**validated_data,)
        return admin

# Admin specific data that should be returned as login reponse
class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = "__all__"

# Admin Details for Admins
class AdminReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields= ["id","email","first_name","last_name","contact_number","image","role","blocked",]

# system report
class SystemReportReadSerializer(serializers.Serializer):
    user_count = serializers.SerializerMethodField(read_only=True)
    student_count = serializers.SerializerMethodField(read_only=True)
    lecturer_count = serializers.SerializerMethodField(read_only=True)
    admin_count = serializers.SerializerMethodField(read_only=True)
    lab_assistant_count = serializers.SerializerMethodField(read_only=True)
    lab_manager_count=serializers.SerializerMethodField(read_only=True)
    total_department_count=serializers.SerializerMethodField(read_only=True)
    total_lab_count=serializers.SerializerMethodField(read_only=True)
    total_category_count=serializers.SerializerMethodField(read_only=True)
    total_display_item_count=serializers.SerializerMethodField(read_only=True)
    total_item_count = serializers.SerializerMethodField(read_only=True)
    available_item_count = serializers.SerializerMethodField(read_only=True)
    borrowed_items_count=serializers.SerializerMethodField(read_only=True)
    temp_borrowed_items_count=serializers.SerializerMethodField(read_only=True)
    damaged_items_count=serializers.SerializerMethodField(read_only=True)

    def get_user_count(self,validated_data):
        user_count = User.objects.all().count()
        return user_count
    
    def get_student_count(self,validated_data):
        student_count = Student.objects.all().count()
        return student_count

    def get_lecturer_count(self,validated_data):
        lecturer_count = Lecturer.objects.all().count()
        return lecturer_count
    
    def get_lab_assistant_count(self,validated_data):
        lab_assistant_count = LabAssistant.objects.all().count()
        return lab_assistant_count
    
    def get_lab_manager_count(self,validated_data):
        lab_manager_count = LabManager.objects.all().count()
        return lab_manager_count
    
    def get_admin_count(self,validated_data):
        admin_count = Admin.objects.all().count()
        return admin_count
    
    def get_total_department_count(self,validated_data):
        total_department_count = Department.objects.all().count()
        return total_department_count

    def get_total_lab_count(self,validated_data):
        total_lab_count = Lab.objects.all().count()
        return total_lab_count

    def get_total_category_count(self,validated_data):
        total_category_count = ItemCategory.objects.all().count()
        return total_category_count

    def get_total_display_item_count(self,validated_data):
        total_display_item_count = DisplayItem.objects.all().count()
        return total_display_item_count

    def get_total_item_count(self,validated_data):
        total_item_count = Item.objects.all().count()
        return total_item_count

    def get_available_item_count(self,validated_data):
        available_item_count = Item.objects.filter(state=State.AVAILABLE).count()
        return available_item_count
    
    def get_borrowed_items_count(self,validated_data):
        borrowed_items_count = Item.objects.filter(state=State.BORROWED).count()
        return borrowed_items_count
    
    def get_temp_borrowed_items_count(self,validated_data):
        temp_borrowed_items_count = Item.objects.filter(state=State.TEMP_BORROWED).count()
        return temp_borrowed_items_count
    
    def get_damaged_items_count(self,validated_data):
        damaged_items_count = Item.objects.filter(state=State.DAMAGED).count()
        return damaged_items_count
    
    