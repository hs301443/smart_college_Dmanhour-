# Generated by Django 5.2 on 2025-05-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_collegeleaders_cv_alter_collegeleaders_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeleaders',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='Collegeleaders/'),
        ),
        migrations.AlterField(
            model_name='collegeleaders',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Collegeleaders/'),
        ),
    ]
