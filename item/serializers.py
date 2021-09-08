import item_category
from django.db.models import fields
from item.models import Item
from lab.serializers import LabReadSerializer
from item_category.serializers import ItemCategoryReadSerializer
from display_item.serializers import DisplayItemReadSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction

#data visible as response
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

#data for creating Item
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

#Editting item is not in system functionalities
        
class ItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=('id','state') # item category must not be editable

