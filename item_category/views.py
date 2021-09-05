from .serializers import ItemCategoryInDepthReadSerializer, ItemCategoryUpdateSerializer, ItemCategoryWriteSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from item_category.models import ItemCategory
from rest_framework import permissions
from custom_user.permissions import IsLabManager
from rest_framework.exceptions import ValidationError

#POST request to create ItemCategory
class ItemCategoryCreateAPIView(CreateAPIView):
    serializer_class=ItemCategoryWriteSerializer
    queryset=ItemCategory.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsLabManager)

#GET request to get all item_categories
class ItemCategoryListAPIView(ListAPIView):
    serializer_class=ItemCategoryInDepthReadSerializer
    queryset=ItemCategory.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

#GET request to get one category
class ItemCategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class=ItemCategoryInDepthReadSerializer
    queryset=ItemCategory.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field='id'

#PUT request to edit labs
class ItemCategoryUpdateAPIView(UpdateAPIView):
    serializer_class=ItemCategoryUpdateSerializer
    queryset=ItemCategory.objects.all()
    permissions_classes=(permissions.IsAuthenticated,IsLabManager)
    lookup_field='id'


# GET request to get categories of a specific lab
class ItemCategoryListByLabAPIView(ListAPIView):
    serializer_class=ItemCategoryInDepthReadSerializer
    queryset=ItemCategory.objects.all()
    permission_classes=(permissions.IsAuthenticated,)

    def get_queryset(self):
        try:
            return self.queryset.filter(lab = self.kwargs.get('lab_id', None)) # get only labs for the passed id in url
        except:
            raise ValidationError("Provided lab id not valid")