from django.urls import path
from .views import ItemCategoryCreateAPIView, ItemCategoryListAPIView, ItemCategoryListByLabAPIView, ItemCategoryRetrieveAPIView, ItemCategoryUpdateAPIView

urlpatterns = [
     path('', ItemCategoryListAPIView.as_view(), name='all-item-categories'),
     path('<str:id>', ItemCategoryRetrieveAPIView.as_view(), name='single-item-category'),
     path('create/',ItemCategoryCreateAPIView.as_view(), name='new-item-category'),
     path('update/<str:id>', ItemCategoryUpdateAPIView.as_view(), name='update-item-category'),
     path('of-lab/<str:lab_id>', ItemCategoryListByLabAPIView.as_view(), name='item-categories-of-a-lab'),
]