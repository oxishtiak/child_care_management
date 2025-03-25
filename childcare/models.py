from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    phone = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.username    
