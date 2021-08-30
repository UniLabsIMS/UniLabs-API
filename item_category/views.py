from item_category.serializers import Item_CategoryInDepthReadSerializer, Item_CategoryReadSerializer, Item_CategoryWriteSerializer
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from item_category.models import Item_Category
from rest_framework import permissions
from custom_user.permissions import IsLabManager


#POST request to create Item_Category
class Item_CategoryCreateAPIView(CreateAPIView):
    serializer_class=Item_CategoryWriteSerializer
    queryset=Item_Category.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabManager)

#GET request to get all item_categories
class Item_CategoryListAPIView(ListAPIView):
    serializer_class=Item_CategoryInDepthReadSerializer
    queryset=Item_Category.objects.all()
    permissions_classes=(permissions.IsAuthenticated)

#GET request to get one category
class Item_CategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class=Item_CategoryInDepthReadSerializer
    queryset=Item_Category.objects.all()
    permissions_classes=(permissions.IsAuthenticated)
    lookup_field='id'

#PUT request to edit lab
class Item_CategoryUpdateAPIView(UpdateAPIView):
    serializer_class=Item_CategoryWriteSerializer
    queryset=Item_Category.objects.all()
    permissions_classes=(permissions.IsAuthenticated,IsLabManager)
    lookup_field='id'