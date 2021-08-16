from django.db import models
from uuid import uuid4

# Department Model.
class Department(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True,editable=False)
    name=models.CharField(max_length=255,unique=True,editable=False)
    
    def __str__(self):
        return 'name'