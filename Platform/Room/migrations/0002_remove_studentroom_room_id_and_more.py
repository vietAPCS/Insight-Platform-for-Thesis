# Generated by Django 5.0.4 on 2024-05-07 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentroom',
            name='room_id',
        ),
        migrations.RemoveField(
            model_name='studentroom',
            name='student_id',
        ),
        migrations.DeleteModel(
            name='ExamRoom',
        ),
        migrations.DeleteModel(
            name='StudentRoom',
        ),
    ]
