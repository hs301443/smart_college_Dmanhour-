# Generated by Django 5.2 on 2025-05-17 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_collegeleaders_cv_alter_facultyinfo_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegeleaders',
            name='cv',
        ),
        migrations.AddField(
            model_name='collegeleaders',
            name='cv_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
