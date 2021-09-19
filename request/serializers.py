from display_item.serializers import DisplayItemReadSerializer
from lab.serializers import LabReadSerializer
from lecturer_user.serializers import LecturerReadSerializer
from django.core.exceptions import ValidationError
from display_item.models import DisplayItem
from django.db.models import fields
from request.models import Request,RequestItem
from rest_framework import serializers
from lecturer_user.models import LabLecturer,Lecturer
from django.db import transaction
from student_user.serializers import StudentReadSerializer

class RequestWriteSerializer(serializers.ModelSerializer):
    display_items_dict=serializers.DictField(child=serializers.IntegerField(),write_only=True)
    class Meta:
        model=Request
        fields=('id','student','lecturer','reason','display_items_dict')
    
    def validate(self,data):
        display_items_dict=data.get('display_items_dict')
        lab=DisplayItem.objects.get(id=str(list(display_items_dict.keys())[0])).lab_id
        lab_lecturers=LabLecturer.objects.filter(lecturer_id=data.get('lecturer'))
        for lab_lecturer in lab_lecturers:
            count=0
            if (lab_lecturer.lab_id==lab):
                count+=1
        if (count==0):
            raise ValidationError("Lecturer should be permmited to the lab")
        for display_item_id in display_items_dict.keys():
            if(not(DisplayItem.objects.filter(id=str(display_item_id)).exists())):
                raise ValidationError("Invalid Display Item id")
            elif (DisplayItem.objects.filter(id=str(display_item_id)).exists()):
                if (DisplayItem.objects.get(id=str(display_item_id)).item_count<display_items_dict[str(display_item_id)]):
                    # import pdb; pdb.set_trace()
                    raise ValidationError("Enough items are not available")
                if (lab!=DisplayItem.objects.get(id=str(display_item_id)).lab_id):
                    raise ValidationError("Per request one lab items can be get")

        return data


    @transaction.atomic
    def create(self,validated_data):
        display_items_dict=validated_data.pop('display_items_dict')
        lab=DisplayItem.objects.get(id=str(list(display_items_dict.keys())[0])).lab
        request=Request.objects.create(lab=lab,**validated_data)
        student=validated_data.get('student')
        

        for display_item_id in display_items_dict.keys():
            display_item=DisplayItem.objects.get(id=str(display_item_id))
            item_count=display_items_dict[str(display_item_id)]
            RequestItem.objects.create(request=request,display_item=display_item,student=student,lab=lab,quentity=item_count)

        return request

class RequestInDepthSerializer(serializers.ModelSerializer):
    lab=LabReadSerializer()
    student=StudentReadSerializer()
    lecturer=LecturerReadSerializer()
    display_items_dict=serializers.SerializerMethodField()

    def get_display_items_dict(self,obj):
        request_items=RequestItem.objects.filter(request=obj)
        display_items=[]

        for request_item_obj in request_items:
            display_items.append(DisplayItemReadSerializer(request_item_obj.display_item).data)
        return display_items
    class Meta:
        model=Request
        fields='__all__'






       
