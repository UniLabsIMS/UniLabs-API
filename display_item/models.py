from django.db import models
from uuid import uuid4

from django.db.models.deletion import CASCADE
from item_category.models import ItemCategory
from lab.models import Lab

# DisplayItem Model

class DisplayItem(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    item_category=models.ForeignKey(ItemCategory,on_delete=CASCADE)
    lab=models.ForeignKey(Lab,on_delete=CASCADE)
    name=models.CharField(max_length=255,blank=False)
    image=models.ImageField(upload_to='display_items',blank=True)
    description=models.CharField(max_length=1023,blank=False)
    item_count=models.IntegerField(blank=False,default=0)
    added_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'name'