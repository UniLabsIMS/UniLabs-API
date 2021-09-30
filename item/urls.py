from django.urls import path
from .views import BorrowLogListofLabAPIView, BorrowLogListofStudentAPIView, CurrentBorrowedItemListofLabAPIView, CurrentBorrowedItemListofStudentAPIView, ItemCreateAPIView, ItemDeleteAPIView,ItemListByLabAPIView, ItemListByItemCategoryAPIView,ItemUpdateAPIView,ItemListAPIView,ItemListByDisplayItemAPIView,ItemRetriveAPIView,TemporaryHandOverItemAPIView,ReturnItemAPIView,BorrowLogListAPIView

urlpatterns=[
    path('',ItemListAPIView.as_view(), name='all-items'),
    path('<str:id>',ItemRetriveAPIView.as_view(), name='single-item'),
    path('create/',ItemCreateAPIView.as_view(), name='new-item'),
    path('update/<str:id>',ItemUpdateAPIView.as_view(),name='update-item'),
    path('delete/<str:id>',ItemDeleteAPIView.as_view(),name='delete-item'),
    path('of-display-item/<str:display_item_id>', ItemListByDisplayItemAPIView.as_view(), name='items-of-a-display-item'),
    path('of-item-category/<str:item_category_id>', ItemListByItemCategoryAPIView.as_view(), name='items-of-an-item-category'),
    path('of-lab/<str:lab_id>', ItemListByLabAPIView.as_view(), name='items-of-a-lab'),
    path('temporary-handover/<str:id>',TemporaryHandOverItemAPIView.as_view(), name='temporary-handover'),
    path('return-item/<str:id>',ReturnItemAPIView.as_view(),name='return-item'),
    path('all-borrow-logs/',BorrowLogListAPIView.as_view(),name='all-borrow-logs'),
    path('all-borrow-logs/of-lab/<str:lab_id>',BorrowLogListofLabAPIView.as_view(),name='all-borrow-logs-of-lab'),
    path('all-borrow-logs/of-student/<str:student_id>',BorrowLogListofStudentAPIView.as_view(),name='all-borrow-logs-of-student'),
    path('borrowed/from-lab/<str:lab_id>',CurrentBorrowedItemListofLabAPIView.as_view(),name='currently-borrowed-from-lab'),
    path('borrowed/by-student/<str:student_id>',CurrentBorrowedItemListofStudentAPIView.as_view(),name='currently-borrowed-by-student'),
]