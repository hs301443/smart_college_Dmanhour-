# Generated by Django 5.2 on 2025-06-11 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_graduation_email_graduation_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graduation',
            name='email',
        ),
        migrations.RemoveField(
            model_name='graduation',
            name='username',
        ),
    ]
