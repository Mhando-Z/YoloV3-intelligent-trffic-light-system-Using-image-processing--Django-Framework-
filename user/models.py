from django.db import models
import uuid

# Create your models here.

class Profile(models.Model):
    Full_name=models.CharField(max_length=2000, null=True, blank=True)
    email=models.CharField(max_length=2000, null=True, blank=True)
    phone=models.CharField(max_length=2000, null=True, blank=True)
    social_fb=models.CharField(max_length=2000, null=True, blank=True)
    social_ig=models.CharField(max_length=2000, null=True, blank=True)
    social_tw=models.CharField(max_length=2000, null=True, blank=True)
    social_ln=models.CharField(max_length=2000, null=True, blank=True)
    job=models.CharField(max_length=2000, null=True, blank=True)
    country=models.CharField(max_length=2000, null=True, blank=True)
    picture=models.ImageField(blank=True, null=True, upload_to='profiles/', default="image/profile/picha.png")
    description=models.TextField(blank=True, null=True)                                                 
    create=models.DateField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.Full_name
       
