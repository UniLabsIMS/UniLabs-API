from request.models import RequestItem, RequestItemState
from student_user.serializers import StudentSummarizedReadSerializer
from item.models import BorrowLog, Item, LogState, State
from lab.serializers import LabReadSerializer
from item_category.serializers import ItemCategoryReadSerializer
from display_item.serializers import DisplayItemReadSerializer
from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from student_user.models import Student
from datetime import date

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

# only expand display item data
class ItemSingleDepthReadSerializer(serializers.ModelSerializer):
    display_item=DisplayItemReadSerializer()

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

#temporary handover serilaizer
class TemporaryHandoverSerializer(serializers.ModelSerializer):
    student_uuid=serializers.CharField(write_only=True)
    class Meta:
        model=Item
        fields=('student_uuid',)
    
    def validate(self,data):
        item=self.instance
        if (item.state)!=State.AVAILABLE:
            raise ValidationError("Item is not available")
        if(not Student.objects.filter(id=data['student_uuid']).exists()):
            raise ValidationError("Invalid student id")
        return data
    
    @transaction.atomic
    def save(self,validated_data):
        item = self.instance
        student=Student.objects.get(user_ptr_id=validated_data['student_uuid'])
        item.state=State.TEMP_BORROWED
        item.save()
        return BorrowLog.objects.create(item=item,lab=item.lab,state=LogState.TEMP_BORROWED,student=student,due_date=date.today())


#return item. borrow log and item state changes
class ItemReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields=[]

    def validate(self,data):
        borrow_log=BorrowLog.objects.filter(item=self.instance.id,state__in=[LogState.BORROWED,LogState.TEMP_BORROWED])
        if (borrow_log.count()==0):
            raise ValidationError("Given item is not borrowed")
        if (borrow_log.count()!=1):
            raise ValidationError("one item can be borrowed by one person only")
        return data
    
    @transaction.atomic
    def save(self,data):
        item = self.instance
        borrow_log=BorrowLog.objects.get(item=item.id,state__in=[LogState.BORROWED,LogState.TEMP_BORROWED])
        item.state=State.AVAILABLE
        item.save()
        borrow_log.state=LogState.RETURNED
        borrow_log.returned_date=date.today()
        borrow_log.save()
        return

#Borrow log Read serializer
class BorrowLogReadSerializer(serializers.ModelSerializer):
    item = ItemSingleDepthReadSerializer()
    student = StudentSummarizedReadSerializer()
    lab = LabReadSerializer()
    class Meta:
        model=BorrowLog
        fields=['id','state','due_date','returned_date','item','student','lab']

# Handover Approved Items Serializer
class HandoverSerializer(serializers.ModelSerializer):
    request_item_id=serializers.CharField(write_only=True)
    due_date=serializers.DateField(write_only=True)
    class Meta:
        model=Item
        fields=('request_item_id','due_date',)
    
    def validate(self,data):
        request_item_id = data.get('request_item_id')
        due_date = data.get('due_date')
        item=self.instance
        if (item.state)!=State.AVAILABLE:
            raise ValidationError("Item is not available")
        try:
            request_item = RequestItem.objects.get(id=request_item_id)
        except Exception as e:
            print(e)
            raise ValidationError("Invalid request item id")
        if(request_item.display_item!=self.instance.display_item):
            raise ValidationError("Parent display item does not match with the item id")
        if(request_item.state!=RequestItemState.APPROVED):
            raise ValidationError("Not allowed to handover non approved items")
        if(request_item.quantity<=0):
            raise ValidationError("Requested Qunatity Already HandedOver")
        if(due_date < date.today()):
            raise ValidationError("Due date should be a date after today")
        return data
    
    @transaction.atomic
    def save(self,validated_data):
        item = self.instance
        request_item=RequestItem.objects.get(id=validated_data['request_item_id'])
        item.state=State.BORROWED
        item.save()
        request_item.quantity -= 1
        if(request_item.quantity==0):
            request_item.state=RequestItemState.COMPLETED
        request_item.save() 
        return BorrowLog.objects.create(item=item,lab=item.lab,state=LogState.BORROWED,student=request_item.student,due_date=validated_data['due_date'])