from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.models import CloudinaryField



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Graduation(models.Model):
    EMPLOYMENT_CHOICES = [
        ('employee', 'موظف'),
        ('unemployee', 'غير موظف'),
        ('freelance', 'يعمل عمل حر'),
        ('postgraduate', 'طالب دراسات عليا'),
        ('seeking_job', 'باحث عن عمل'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='graduation')
    cv = CloudinaryField(resource_type='raw', folder='damanour/Graduation/pdfs', blank=True, null=True)
    employment_status = models.CharField(max_length=100, choices=EMPLOYMENT_CHOICES)
    job_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    company_email = models.EmailField(blank=True)
    company_phone = models.CharField(max_length=20, blank=True)
    company_link = models.URLField(blank=True)
    about_company = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Graduation Info for {self.user.username}"





class Staff(models.Model):
    name= models.CharField(max_length=100)
    position= models.CharField(max_length=100)
    cv = CloudinaryField(
        resource_type='raw', 
        folder='damanhour/Staff/pdfs',
        blank=True, null=True,
        overwrite=True,
        )
    image= models.ImageField(storage=MediaCloudinaryStorage(),upload_to='damanhour/staff_images/', blank=True, null=True)
    department=models.ManyToManyField('academics.Department', blank=True, related_name='staffs')
    units=models.ManyToManyField('units.unit', blank=True, related_name='staffs')

    def __str__(self):
     return f"Staff Member: {self.name}, Position: {self.position}"
