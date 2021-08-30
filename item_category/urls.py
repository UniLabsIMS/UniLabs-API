from django.urls import path,include
from . import views

urlpatterns = [
     path('',views.Item_CategoryListAPIView.as_view(), name='all_item_categories'),
     path('<str:id>', views.Item_CategoryRetrieveAPIView.as_view(), name='single-item_category'),
     path('create/',views.Item_CategoryCreateAPIView.as_view(), name='item_category-create'),
     path('update/<str:id>', views.Item_CategoryUpdateAPIView.as_view(), name='item_category-update')
]