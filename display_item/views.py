from django.shortcuts import render
from rest_framework.serializers import Serializer
from .serializers import DisplayItemInDepthReadSerializer, DisplayItemUpdateSerializer,DisplayItemWriteSerializer,DisplayItemReadSerializer
from display_item.models import DisplayItem
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView
from rest_framework import permissions
from custom_user.permissions import IsLabManager
from rest_framework.exceptions import ValidationError

#POST request to create DisplayItem
class DisplayItemCreateAPIView(CreateAPIView):
    serializer_class=DisplayItemWriteSerializer
    queryset=DisplayItem.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabManager)

#GET request to get all display_items
class DisplayItemListAPIView(ListAPIView):
    serializer_class=DisplayItemInDepthReadSerializer
    queryset=DisplayItem.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

#GET request to get one DisplayItem
class DisplayRetrieveAPIView(RetrieveAPIView):
    serializer_class=DisplayItemInDepthReadSerializer
    queryset=DisplayItem.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field='id'

#PUT request to edit display_item
class DisplayItemUpdateAPIView(UpdateAPIView):
    serializer_class=DisplayItemUpdateSerializer
    queryset=DisplayItem.objects.all()
    permissions_classes=(permissions.IsAuthenticated,IsLabManager)
    lookup_field='id'

#GET request to get display_items of a specific item_category
class DisplayItemListByItemCategoryAPIView(ListAPIView):
    serializer_class=DisplayItemInDepthReadSerializer
    queryset=DisplayItem.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(item_category=self.kwargs.get('item_category_id',None)) # get only item_category for the passed id in url
        except:
            raise ValidationError('Provided item category id not valid')