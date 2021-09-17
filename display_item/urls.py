from django.urls import path
from .views import DisplayItemCreateAPIView,DisplayItemListAPIView,DisplayItemListByLabAPIView,DisplayRetrieveAPIView,DisplayItemUpdateAPIView,DisplayItemListByItemCategoryAPIView

urlpatterns=[
    path('',DisplayItemListAPIView.as_view(), name='all-display-items'),
    path('<str:id>',DisplayRetrieveAPIView.as_view(), name='single-display-item'),
    path('create/',DisplayItemCreateAPIView.as_view(), name='new-display-item'),
    path('update/<str:id>', DisplayItemUpdateAPIView.as_view(),name='update-display-item'),
    path('of-item-category/<str:item_category_id>', DisplayItemListByItemCategoryAPIView.as_view(), name='display-items-of-a-item-category'),
    path('of-lab/<str:lab_id>', DisplayItemListByLabAPIView.as_view(), name='display-items-of-a-lab'),
]