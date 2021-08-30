from lab.serializers import LabReadSerializer
from .models import Item_Category
from rest_framework import serializers

#data visible as the response
class Item_CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Category
        fields="__all__"
        
class Item_CategoryInDepthReadSerializer(serializers.ModelSerializer):
    lab=LabReadSerializer()
    class Meta:
        model = Item_Category
        fields="__all__"
    

#data for editing and creating Item_Category
class Item_CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_Category
        fields=('id','lab','name','description',)# id wont show up as required, as editable is set to false
