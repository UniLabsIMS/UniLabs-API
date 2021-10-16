from custom_user.utils.email import Email
import pdb
from display_item.serializers import DisplayItemReadSerializer
from lab.models import Lab
from lab.serializers import LabReadSerializer
from lecturer_user.serializers import LecturerSummarizedReadSerializer
from django.core.exceptions import ValidationError
from display_item.models import DisplayItem
from request.models import Request,RequestItem, RequestItemState, RequestState
from rest_framework import serializers
from lecturer_user.models import LabLecturer
from django.db import transaction
from student_user.serializers import StudentReadSerializer
from django.db import transaction
class RequestWriteSerializer(serializers.ModelSerializer):
    display_items_dict=serializers.DictField(child=serializers.IntegerField(),write_only=True)
    class Meta:
        model=Request
        fields=('id','student','lecturer','lab','reason','display_items_dict')
    
    def validate(self,data):
        display_items_dict=data.get('display_items_dict') # pop the display items dictionary
        
        if(len(display_items_dict)==0):
            raise ValidationError("items requested cannot be empty")

        if(Request.objects.filter(student=data.get('student'),lab=data.get('lab'),state=RequestState.NEW).exists()): # one student can have one pending request per lab
             raise ValidationError("Student already has a pending request for the lab")

        if (not LabLecturer.objects.filter(lecturer=data.get('lecturer'),lab=data.get('lab')).exists()): # check wehther the lecturer has permission
            raise ValidationError("Lecturer should be permmited to the lab")

        for display_item_id in display_items_dict.keys():
            result_lst = DisplayItem.objects.filter(id=str(display_item_id),lab=data.get('lab')) # try to get display item

            if( result_lst.count() == 0): # if no such display item 
                raise ValidationError("Invalid Display Item ID")
            else :
                if (result_lst[0].item_count < display_items_dict[str(display_item_id)]): # check whether requested amount is less than available
                    raise ValidationError("Enough items are not available")

                if(display_items_dict[str(display_item_id)]<=0): # check whether request count is 0 or less
                    raise ValidationError("Requested quantity for each display item must be greater than zero")

        return data


    @transaction.atomic
    def create(self,validated_data):
        display_items_dict=validated_data.pop('display_items_dict')
        request=Request.objects.create(**validated_data)
        student=validated_data.get('student')
        lab = validated_data.get('lab')
        
        for display_item_id in display_items_dict.keys():
            display_item=DisplayItem.objects.get(id=str(display_item_id))
            item_count=display_items_dict[str(display_item_id)]
            RequestItem.objects.create(request=request,display_item=display_item,student=student,lab=lab,quantity=item_count)
        
        try:
            Email.send_new_request_email(validated_data.get('lecturer').email)
        except Exception as e:
            raise Exception('Error sending new request email')

        return request

# display request item data in get requests
class RequestItemReadSerializer(serializers.ModelSerializer):
    display_item = DisplayItemReadSerializer()
    class Meta:
        model=RequestItem
        fields=("id","display_item","quantity","state")

class RequestInDepthSerializer(serializers.ModelSerializer):
    lab=LabReadSerializer()
    student=StudentReadSerializer()
    lecturer=LecturerSummarizedReadSerializer()
    requested_display_items=serializers.SerializerMethodField()

    def get_requested_display_items(self,obj):
        request_items=RequestItem.objects.filter(request=obj)
        requested_display_items=[]

        for request_item_obj in request_items:
            requested_display_items.append(RequestItemReadSerializer(instance=request_item_obj).data)
        return requested_display_items
    class Meta:
        model=Request
        fields='__all__'

#approve or decline request functionalities serializer
class UpdateRequestStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields=("state",)

    def validate(self,data): #to makie sure contact number is only digits
        if not(((data.get('state'))==RequestState.APPROVED) or ((data.get('state'))==RequestState.DECLINED)):
            raise ValidationError("Only Approved and Declined State changes can be done")
        
        if self.instance.state!=RequestState.NEW:
            raise ValidationError("Initial Request state should be New")
        return data
    
    @transaction.atomic
    def save(self,data):
        request = self.instance
        request.state=data.get('state')
        request.save()
        request_items = RequestItem.objects.filter(request=request)
        for req_item in request_items:
            req_item.state = data.get('state') 
            req_item.save()
        try:
            Email.send_request_approve_decline(request.student.email,data.get('state'),request.lab.name)
        except Exception as e:
            raise Exception('Error sending request approve decline')
        return

class ClearApprovedRequestItemsFromLabForStudentSerailizer(serializers.ModelSerializer):
    student = serializers.CharField(write_only=True)
    lab = serializers.CharField(write_only=True)
    class Meta:
        model = RequestItem
        fields = ['student','lab']
    
    @transaction.atomic
    def save(self,data):
        approved_request_items= RequestItem.objects.filter(student=data.get('student'),lab=data.get('lab'),state=RequestItemState.APPROVED)
        for request_item in approved_request_items:
            request_item.state=RequestItemState.DECLINED_BY_LAB
            request_item.save()
        return


class StudentCheckForActiveRequestInLabSerializer(serializers.Serializer):
    state = serializers.SerializerMethodField(read_only=True)
    lab_id = serializers.CharField(write_only=True)
    student_id = serializers.CharField(write_only=True)

    def validate(self, data):
        lab_id=data.get('lab_id')
        student_id=data.get('student_id')
        try:
            lab=Lab.objects.get(id=lab_id)
        except:
            raise ValidationError('Lab id should be valid id')

        return data
    
    def get_state(self,validated_data):
        lab_id=validated_data.get('lab_id')
        student_id=validated_data.get('student_id')
        count=Request.objects.filter(lab=lab_id,student=student_id,state=RequestState.NEW).count()
        return count > 0

        


       
