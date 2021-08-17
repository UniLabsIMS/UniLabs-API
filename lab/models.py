from django.db import models
from uuid import uuid4
from department.models import Department

# Lab Model.
class Lab(models.Model):
    lab_id = models.UUIDField(default=uuid4, primary_key=True,editable=False)
    name = models.CharField(max_length=255,unique=True,editable=False)
    department_name = models.ForeignKey(Department,to_field='name', on_delete=models.CASCADE)
    location=models.CharField(max_length=1023,blank=True)
    contact_no=models.CharField(max_length=255,blank=True)
    contact_email=models.EmailField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return 'name'
