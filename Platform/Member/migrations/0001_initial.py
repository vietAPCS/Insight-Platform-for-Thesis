# Generated by Django 5.0.4 on 2024-05-03 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Community', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('MetamarskID', models.CharField(max_length=255)),
                ('avatar', models.ImageField(default='default.png', upload_to='profile_images')),
                ('userid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCommunity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(blank=True, default=10, null=True)),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('is_mentor', models.BooleanField(blank=True, default=False)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestMentor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('upadate_date', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(blank=True, default=0, null=True)),
                ('UserCommunityId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_in_community', to='Member.usercommunity')),
                ('mentorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requesting_mentors', to='Member.usercommunity')),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('update_date', models.DateField(auto_now_add=True)),
                ('content', models.CharField(max_length=255)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
