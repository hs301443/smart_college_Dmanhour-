from django.db import models
from apps.users.models import CustomUser
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.
class Studentprtal(models.Model):
    types=models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(storage=MediaCloudinaryStorage(),upload_to='damanhour/Studentportal/', blank=True, null=True)  
    link = models.URLField(max_length=255, blank=True, null=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
class StudentPortalImage(models.Model):
    portal = models.ForeignKey(Studentprtal, on_delete=models.CASCADE, related_name="extra_images")
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/Studentportal/multiple/',
        blank=False, null=False
    )
    
    
    
    
    
# notifications/models.py

class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    send_to_all = models.BooleanField(default=False)

    def __str__(self):
        return self.title
