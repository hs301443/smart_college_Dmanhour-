from django.db import models

from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.models import CloudinaryField

class VisionMission(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(
        upload_to='damanhour/VisionMission/images/',
        storage=MediaCloudinaryStorage(),
        blank=True, null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class slider(models.Model):
    title = models.CharField(max_length=255)
    video = CloudinaryField(
        resource_type='video',
        folder='damanhour/slider/videos/',
        blank=True, null=True
    )

    def __str__(self):
      return self.title or "No title"




class FacultyInfo(models.Model):  
    title = models.CharField(max_length=255)
    content = models.TextField()
    video = CloudinaryField(
        resource_type='video',
        folder='damanhour/FacultyInfo/videos/',
        blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Statistics(models.Model):
    title = models.CharField(max_length=255, default='إحصائيات كلية الحاسبات والمعلومات', editable=False)  # تم تغيير النص
    instructors = models.PositiveIntegerField()
    students = models.PositiveIntegerField()
    managers = models.PositiveIntegerField()
    masters_students = models.PositiveIntegerField()

#abour college
class Collegeleaders(models.Model):
    position = models.CharField(max_length=255)
    name= models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(
        upload_to='damanhour/Collegeleaders/images/',
        storage=MediaCloudinaryStorage(),
        blank=True, null=True,
    )
    
    cv = models.URLField(blank=True, null=True)


    def __str__(self):                                                          
        return self.position 
    
    
    
    
    
    
    
    
#الشكاوى والمقترحات


class Complaint(models.Model):
   

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=255)
    content = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"