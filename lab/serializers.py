from django.db.models.fields.related import RelatedField
from .models import Lab
from rest_framework import serializers,viewsets

#data visible as the response
class LabReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lab
        fields='__all__'

#data for editing and creating lab
class LabWriteSerializer(serializers.ModelSerializer):
    name=serializers.CharField(max_length=255)
    location=serializers.CharField(max_length=1023)
    contact_no=serializers.CharField(max_length=255)
    contact_email=serializers.EmailField(max_length=255)

    class Meta:
        model = Lab
        fields=('name','department_name','location','contact_no','contact_email',)