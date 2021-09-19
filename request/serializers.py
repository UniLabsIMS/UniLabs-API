from display_item.serializers import DisplayItemReadSerializer
from lab.serializers import LabReadSerializer
from lecturer_user.serializers import LecturerReadSerializer
from django.core.exceptions import ValidationError
from display_item.models import DisplayItem
from django.db.models import fields
from request.models import Request,RequestItem, RequestState
from rest_framework import serializers
from lecturer_user.models import LabLecturer,Lecturer
from django.db import transaction
from student_user.serializers import StudentReadSerializer

class RequestWriteSerializer(serializers.ModelSerializer):
    display_items_dict=serializers.DictField(child=serializers.IntegerField(),write_only=True)
    class Meta:
        model=Request
        fields=('id','student','lecturer','lab','reason','display_items_dict')
    
    def validate(self,data):
        display_items_dict=data.get('display_items_dict') # pop the display items dictionary

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
                    raise ValidationError("Requested qunatity for each display item must be greater than zero")

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

        return request


# display request item data in get requests
class RequestItemReadSerializer(serializers.ModelSerializer):
    display_item = DisplayItemReadSerializer()
    class Meta:
        model=RequestItem
        fields=("display_item","quantity","state")

class RequestInDepthSerializer(serializers.ModelSerializer):
    lab=LabReadSerializer()
    student=StudentReadSerializer()
    lecturer=LecturerReadSerializer()
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






       
