from lab.serializers import LabReadSerializer
from .models import ItemCategory
from rest_framework import serializers

#data visible as the response
class ItemCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields="__all__"
        
class ItemCategoryInDepthReadSerializer(serializers.ModelSerializer):
    lab=LabReadSerializer()
    class Meta:
        model = ItemCategory
        fields="__all__"
    

#data for editing and creating ItemCategory
class ItemCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields=('id','lab','name','description',)# id wont show up as required, as editable is set to false
