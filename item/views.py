from rest_framework.serializers import Serializer
from lab_assistant_user.models import LabAssistant
from rest_framework import generics
from rest_framework.generics import CreateAPIView, GenericAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework import permissions,generics
from custom_user.permissions import IsLabAssistant, IsLabManagerOrAssistant, IsLabOwner
from rest_framework.exceptions import ValidationError
from .serializers import BorrowLogReadSerializer, HandoverSerializer, ItemInDepthReadSerializer,ItemWriteSerializer,ItemUpdateSerializer,TemporaryHandoverSerializer,ItemReturnSerializer
from  item.models import BorrowLog, Item, LogState
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from display_item.models import DisplayItem

#POST request to create Item
class ItemCreateAPIView(CreateAPIView):
    serializer_class=ItemWriteSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabManagerOrAssistant)

#GET request to get all items
class ItemListAPIView(ListAPIView):
    serializer_class=ItemInDepthReadSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

#GET request to one item
class ItemRetriveAPIView(RetrieveAPIView):
    serializer_class=ItemInDepthReadSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field='id'

#PUT request to edit item
class ItemUpdateAPIView(UpdateAPIView):
    serializer_class=ItemUpdateSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabAssistant, IsLabOwner)  #Lab assistant only can toggle states
    lookup_field='id'

#GET request to get items of a specific display_item
class ItemListByDisplayItemAPIView(ListAPIView):
    serializer_class=ItemInDepthReadSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(display_item=self.kwargs.get('display_item_id',None)) # get only items for the passed id in url
        except:
            raise ValidationError('Provided display item id not valid')

#GET request to get items of a specific item_category
class ItemListByItemCategoryAPIView(ListAPIView):
    serializer_class=ItemInDepthReadSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(item_category=self.kwargs.get('item_category_id',None)) # get only items for the passed id in url
        except:
            raise ValidationError('Provided item category id not valid')

#GET request to get items of a specific lab
class ItemListByLabAPIView(ListAPIView):
    serializer_class=ItemInDepthReadSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(lab=self.kwargs.get('lab_id',None)) # get only items for the passed id in url
        except:
            raise ValidationError('Provided lab id not valid')

#DELETE request to delete item
class ItemDeleteAPIView(DestroyAPIView): # no need to serialize
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabManagerOrAssistant, IsLabOwner)
    lookup_field='id'

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        display_item = DisplayItem.objects.get(id=item.display_item.id)
        display_item.item_count -=1
        display_item.save()
        item.delete()
        return Response("Item deleted", status=status.HTTP_204_NO_CONTENT)

# view to temp handover item 
class TemporaryHandOverItemAPIView(GenericAPIView):
    serializer_class=TemporaryHandoverSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabAssistant, IsLabOwner)
    lookup_field='id'

    @transaction.atomic
    def post(self,request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(data=request.data,instance=item)
        if serializer.is_valid():
            serializer.save(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# return item
class ReturnItemAPIView(GenericAPIView):
    serializer_class=ItemReturnSerializer
    permission_classes=(permissions.IsAuthenticated,IsLabAssistant,IsLabOwner)
    queryset=Item.objects.all()
    lookup_field='id'

    def put(self,request, *args, **kwargs):
        item=self.get_object()
        serializer=self.get_serializer(data=request.data,instance=item)
        if serializer.is_valid():
            serializer.save(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#GET request to get all borrow logs
class BorrowLogListAPIView(ListAPIView):
    serializer_class=BorrowLogReadSerializer
    queryset=BorrowLog.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

#GET request to get all borrow logs
class BorrowLogListofLabAPIView(ListAPIView):
    serializer_class=BorrowLogReadSerializer
    queryset=BorrowLog.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
            try:
                return self.queryset.filter(lab_id=self.kwargs.get('lab_id',None)) 
            except:
                raise ValidationError('Provided item lab id not valid')

class CurrentBorrowedItemListofLabAPIView(ListAPIView):
    serializer_class=BorrowLogReadSerializer
    queryset=BorrowLog.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
            try:
                return self.queryset.filter(lab_id=self.kwargs.get('lab_id',None),state__in=[LogState.BORROWED,LogState.TEMP_BORROWED]) 
            except:
                raise ValidationError('Provided item lab id not valid')

class BorrowLogListofStudentAPIView(ListAPIView):
    serializer_class=BorrowLogReadSerializer
    queryset=BorrowLog.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
            try:
                return self.queryset.filter(student_id=self.kwargs.get('student_id',None)) 
            except:
                raise ValidationError('Provided item student id not valid')

class CurrentBorrowedItemListofStudentAPIView(ListAPIView):
    serializer_class=BorrowLogReadSerializer
    queryset=BorrowLog.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
            try:
                return self.queryset.filter(student_id=self.kwargs.get('student_id',None),state__in=[LogState.BORROWED,LogState.TEMP_BORROWED]) 
            except:
                raise ValidationError('Provided item student id not valid')

# view to handover item 
class HandOverItemAPIView(GenericAPIView):
    serializer_class=HandoverSerializer
    queryset=Item.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabAssistant, IsLabOwner)
    lookup_field='id'

    @transaction.atomic
    def post(self,request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(data=request.data,instance=item)
        if serializer.is_valid():
            serializer.save(request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)