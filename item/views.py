from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework import permissions
from custom_user.permissions import IsLabAssistant, IsLabManagerOrAssistant
from rest_framework.exceptions import ValidationError
from .serializers import ItemInDepthReadSerializer,ItemWriteSerializer,ItemUpdateSerializer
from  item.models import Item

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
    permissions_classes=(permissions.IsAuthenticated,IsLabAssistant)  #Lab assistant only can toggle states
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
    permission_classes=(permissions.IsAuthenticated,IsLabManagerOrAssistant)
    lookup_field='id'
