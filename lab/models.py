from django.db import models
from uuid import uuid4
from department.models import Department

# Lab Model.
class Lab(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,editable=False)
    name = models.CharField(max_length=255,unique=True)
    department= models.ForeignKey(Department, on_delete=models.CASCADE)
    location=models.CharField(max_length=1023,blank=True)
    contact_no=models.CharField(max_length=255,blank=True)
    contact_email=models.EmailField(max_length=255,blank=True)
    image = models.ImageField(upload_to='labs/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return 'name'
    
    class Meta:
        db_table = 'lab'
