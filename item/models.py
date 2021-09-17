from django.db import models
from uuid import uuid4
from django.utils.http import int_to_base36

from display_item.models import DisplayItem
from lab.models import Lab
from item_category.models import ItemCategory
from django.utils.translation import gettext_lazy as _
from django.db.models.deletion import CASCADE

#State field options for item
class State(models.TextChoices):
    AVAILABLE='Available', _('Available')
    BORROWED='Borrowed', _('Borrowed')
    TEMP_BORROWED='Temp_Borrowed', _('Temp_Borrowed')
    DAMAGED='Damaged', _('Damaged')

ID_LENGTH = 9

# Generates random string whose length is `ID_LENGTH`
def id_gen() -> str:
    return int_to_base36(uuid4().int)[:ID_LENGTH]
    
#Item Model
class Item(models.Model):
    id = models.CharField(primary_key=True, default=id_gen, editable=False,max_length=ID_LENGTH)
    display_item=models.ForeignKey(DisplayItem,on_delete=CASCADE)
    item_category=models.ForeignKey(ItemCategory,on_delete=CASCADE)
    lab=models.ForeignKey(Lab,on_delete=CASCADE)
    state=models.CharField(max_length=31,choices=State.choices,default='Available')
    added_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id'   
    
    class Meta:
        db_table = 'item'

