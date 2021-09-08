from django.urls import path
from .views import ItemCreateAPIView,ItemUpdateAPIView,ItemListAPIView,ItemListByDisplayItemAPIView,ItemRetriveAPIView

urlpatterns=[
    path('',ItemListAPIView.as_view(), name='all-items'),
    path('<str:id>',ItemRetriveAPIView.as_view(), name='single-item'),
    path('create/',ItemCreateAPIView.as_view(), name='new-item'),
    path('update/<str:id>',ItemUpdateAPIView.as_view(),name='update-item'),
    path('of-display-item/<str:display_item_id>', ItemListByDisplayItemAPIView.as_view(), name='items-of-a-display-item'),
]