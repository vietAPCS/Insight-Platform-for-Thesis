# Generated by Django 5.0.4 on 2024-05-03 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='avatar',
        ),
    ]
