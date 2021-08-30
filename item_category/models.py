from django.db.models.deletion import CASCADE
from lab.models import Lab
from django.db import models
from uuid import uuid4

# Item_Category Model

class Item_Category(models.Model):
    id=models.UUIDField(default=uuid4, primary_key=True,editable=False)
    lab=models.ForeignKey(Lab,on_delete=CASCADE)
    name=models.CharField(max_length=255,blank=False)
    image=models.ImageField(upload_to='item_categories',blank=True)
    description=models.CharField(max_length=1023,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'name'

