# Generated by Django 5.0.4 on 2024-05-25 06:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Community', '0003_alter_community_member_alter_community_created_user_and_more'),
        ('Room', '0004_remove_studentroom_room_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRoom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('final_grade', models.IntegerField(blank=True, default=10, null=True)),
                ('former_signature', models.TextField(blank=True, max_length=255)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_cid', models.TextField(blank=True, max_length=255)),
                ('answer_cid', models.TextField(blank=True, max_length=255)),
                ('grade', models.IntegerField(blank=True, default=0)),
                ('student_signature', models.TextField(blank=True, max_length=255)),
                ('mentor_signature', models.TextField(blank=True, max_length=255)),
                ('mentor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Room.examroom')),
            ],
        ),
        migrations.AddField(
            model_name='examroom',
            name='detail',
            field=models.ManyToManyField(related_name='room_detail', through='Room.RoomDetails', to=settings.AUTH_USER_MODEL),
        ),
    ]
