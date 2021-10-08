from django.db.models import fields
import item_category
from lab.serializers import LabReadSerializer
from item_category.serializers import ItemCategoryReadSerializer
from .models import DisplayItem
from rest_framework import serializers
from item_category.models import ItemCategory
from rest_framework.exceptions import ValidationError

#data visible as response
class DisplayItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model=DisplayItem
        fields="__all__"

class DisplayItemInDepthReadSerializer(serializers.ModelSerializer):
    item_category=ItemCategoryReadSerializer()
    lab=LabReadSerializer()

    class Meta:
        model=DisplayItem
        fields='__all__'

#data for creating DisplayItem
class DisplayItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=DisplayItem
        fields=('id','item_category','name','description','image') # id wont show up as required, as editable is set to false

    # setting the lab column using the item_category field
    def create(self,validated_data): 
        lab = validated_data.get('item_category').lab
        return DisplayItem.objects.create(lab=lab,**validated_data)


#data for editting  DisplayItem
class DisplayItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=DisplayItem
        fields=('id','name','description') # item category must not be editable

