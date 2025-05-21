from django.db import models
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.models import CloudinaryField

class section(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='damanhour/Section/images/',
        storage=MediaCloudinaryStorage(),
        blank=True, null=True,
    )
    link = models.URLField(blank=True, null=True)
    pdf = CloudinaryField(
        upload_to='damanhour/Section/pdfs/',
        storage=MediaCloudinaryStorage(),
        blank=True, null=True,
    )

    def __str__(self):
        return self.name


class acadmic_year(models.Model):
    year = CloudinaryField(max_length=255, unique=True)
    lecture_schedule = models.FileField(
        upload_to='damanhour/academic_years/lecture_schedule/',
        storage=MediaCloudinaryStorage(),
        blank=True, null=True,
    )
    practical_exam = CloudinaryField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/academic_years/practical_exam/',
        blank=True, null=True,
    )
    exam = CloudinaryField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/academic_years/exam/',
        blank=True, null=True,
        
    )
    seating_number =CloudinaryField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/academic_years/seating_number/',
        blank=True, null=True,
    )

    def __str__(self):
        return self.year
