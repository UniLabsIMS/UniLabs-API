from item.models import Item
from lab.serializers import LabReadSerializer
from item_category.serializers import ItemCategoryReadSerializer
from display_item.serializers import DisplayItemReadSerializer
from rest_framework import serializers
from django.db import transaction

# Data visible as response
class ItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields="__all__"

class ItemInDepthReadSerializer(serializers.ModelSerializer):
    display_item=DisplayItemReadSerializer()
    item_category=ItemCategoryReadSerializer()
    lab=LabReadSerializer()

    class Meta:
        model=Item
        fields='__all__'

# Data for creating Item
class ItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=('id','display_item')

     #setting the lab column and item_category coloum using the display_item
    @transaction.atomic
    def create(self,validated_data):
        display_item=validated_data.get('display_item')
        item_category=display_item.item_category
        lab=display_item.lab

        display_item.item_count+=1
        display_item.save()

        return Item.objects.create(item_category=item_category,lab=lab,**validated_data)


# Update State        
class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=('id','state') 

# create temporary handover serilaizer
''' 
model -> Item
fields -> student
validate -> check wther the current item state is available
save -> change item state to temp borrow state, add a new borrow log object in atomic manner 


class TempHandoverSerializer(serializers.ModelSerializer):
    student_id = serializers.StringField(write_only=True)
    class Meta:
        model=Item
        fields=('student_id') 
'''