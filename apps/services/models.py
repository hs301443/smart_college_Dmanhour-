from django.db import models

class section(models.Model):
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Unites/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    pdf = models.FileField(upload_to='section/', blank=True, null=True)

    def __str__(self):
        return self.name




class acadmic_year(models.Model):
    year = models.CharField(max_length=255, unique=True)
    leacture_schedule= models.FileField(upload_to='acadmic_years/leacture_schedule/', blank=True, null=True)
    partical_exam= models.FileField(upload_to='acadmic_years/partical_exam/', blank=True, null=True)
    exam= models.FileField(upload_to='acadmic_years/exam/', blank=True, null=True)
    seating_number= models.FileField(upload_to='acadmic_years/seating_number/', blank=True, null=True)
    

    def __str__(self):
        return self.year