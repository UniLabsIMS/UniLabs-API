from django.db.models.manager import BaseManager
from display_item.models import DisplayItem
from lecturer_user.models import LabLecturer, Lecturer
from student_user.models import Student
from django.db.models.deletion import CASCADE
from lab.models import Lab
from django.db import models
from uuid import uuid4
from django.utils.http import int_to_base36
from django.utils.translation import gettext_lazy as _

#state field options for request
class RequestState (models.TextChoices):
    NEW='New',_('New')
    APPROVED='Approved',_('Approved')
    DECLINED='Declined',_('Declined')

#state field options for request item
class RequestItemState (models.TextChoices):
    PENDING='Pending',_('Pending')
    APPROVED='Approved',_('Approved')
    DECLINED='Declined',_('Declined')
    COMPLETED='Completed',_('Completed')

#Request Model
class Request(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    lab=models.ForeignKey(Lab,on_delete=CASCADE)
    student=models.ForeignKey(Student,on_delete=CASCADE)
    lecturer=models.ForeignKey(Lecturer,on_delete=CASCADE)
    reason=models.CharField(max_length=1023,blank=False)
    state=models.CharField(max_length=31,choices=RequestState.choices,default='New')
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id'
    
    class Meta:
        db_table='request'

#Request Item Model
class RequestItem(models.Model):
    id=models.UUIDField(default=uuid4,primary_key=True,editable=False)
    request=models.ForeignKey(Request,on_delete=CASCADE)
    display_item=models.ForeignKey(DisplayItem,on_delete=CASCADE)
    student=models.ForeignKey(Student,on_delete=CASCADE)
    lab=models.ForeignKey(Lab,on_delete=CASCADE)
    quentity=models.IntegerField()
    state=models.CharField(max_length=31,choices=RequestItemState.choices,default='PENDING')

    def __str__(self):
        return 'id'
    
    class Meta:
        db_table='request_item'


