from lecturer_user.serializers import LecturerReadSerializer
from django.core.exceptions import ValidationError
from display_item.models import DisplayItem
from django.db.models import fields
from request.models import Request,RequestItem
from rest_framework import serializers
from lecturer_user.models import LabLecturer,Lecturer

class RequestWriteSerializer(serializers.ModelSerializer):
    display_items_dict=serializers.DictField(child=serializers.IntegerField(),write_only=True)
    class Meta:
        model=Request
        fields=['id','student','lecturer','reason','display_items_dict']
    
    def validate(self,data):
        display_items_dict=data.get('display_items_dict')
        lab=DisplayItem.objects.get(id=list(display_items_dict.keys())[0]).lab
        for display_item_id in display_items_dict.keys():
            if(not(DisplayItem.objects.filter(id=display_item_id).exists())):
                raise ValidationError("Invalid Display Item id")
            elif (DisplayItem.objects.filter(id=display_item_id).exists()):
                if (DisplayItem.objects.get(id=display_item_id).item_count<display_items_dict[display_item_id]):
                    raise ValidationError("Enough items are not available")
                if (lab!=DisplayItem.objects.get(id=display_item_id).lab):
                    raise ValidationError("Per request one lab items can be get")

        return data


    
    def create(self,validated_data):
        display_items_dict=validated_data.pop('display_items_dict')
        lab=DisplayItem.objects.get(id=list(display_items_dict.keys())[0]).lab
        request=Request.objects.create(lab=lab,**validated_data)
        student=validated_data.get('student')
        

        for display_item_id in display_items_dict.keys():
            display_item=DisplayItem.objects.get(id=display_item_id)
            item_count=display_items_dict[display_item_id]
            RequestItem.objects.create(request=request,student=student,lab=lab,display_item=display_item,quentity=item_count)

        return request



       
