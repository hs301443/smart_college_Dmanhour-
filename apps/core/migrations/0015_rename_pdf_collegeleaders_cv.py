# Generated by Django 5.2 on 2025-05-17 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_collegeleaders_cv_collegeleaders_pdf_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collegeleaders',
            old_name='pdf',
            new_name='cv',
        ),
    ]
