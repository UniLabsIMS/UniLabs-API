from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="UniLabs API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.test.com/policies/terms/",
      contact=openapi.Contact(email="contact@test.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # main routes
    path('auth/', include('custom_user.urls')),
    path('admins/', include('admin_user.urls')),
    path('departments/',include('department.urls')),
    path('labs/',include('lab.urls')),
    path('lab-managers/',include('lab_manager_user.urls')),
    path('lab-assistants/',include('lab_assistant_user.urls')),
    path('categories/',include('item_category.urls')),
    path('display-items/',include('display_item.urls')),
    path('students/', include('student_user.urls')),
    path('items/',include('item.urls')),

    # Swagger Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'), # to download documentation
    
    
]
