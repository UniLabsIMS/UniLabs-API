from django.db.models import fields
import item_category
from lab.serializers import LabReadSerializer
from item_category.serializers import ItemCategoryReadSerializer
from .models import DisplayItem
from rest_framework import serializers

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

#data for editting and creating DisplayItem
class DisplayItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=DisplayItem
        fields=('id','item_category','lab','name','description','item_count') # id wont show up as required, as editable is set to false


