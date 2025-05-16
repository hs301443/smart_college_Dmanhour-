from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage

class Department(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    doctors = models.ManyToManyField('users.Staff', related_name='assisting_department', blank=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/department/images/',  # هنا بتحدد الفولدر
        blank=True,
        null=True
    )
    pdf = models.FileField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/department/pdfs/',   # فولدر الملفات PDF
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SpecialProgram(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/Special_Program/images/',  # هنا بتحدد الفولدر
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Special Program: {self.name}"


class MastersProgram(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='damanhour/Masters_Program/images/',  # هنا بتحدد الفولدر
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Masters Program: {self.name}"
