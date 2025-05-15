from django.db import models


class unit(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Unites/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Unnamed Unit"




class UnitService(models.Model):
    unit = models.ForeignKey(unit, on_delete=models.CASCADE, related_name='services')
    about_unit = models.TextField(blank=True, null=True)
    orgnization_structure = models.ManyToManyField('users.Staff', blank=True, related_name='unit_services')
    unit_objectives = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} - {self.unit.name}"