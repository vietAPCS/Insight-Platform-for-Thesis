# Generated by Django 5.0.4 on 2024-05-03 13:55

import Community.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('upload_permission', models.IntegerField(blank=True, default=1, null=True)),
                ('mentor_threshold', models.IntegerField(default=0, validators=[Community.models.validate_no_negative])),
                ('entrance_test_enable', models.BooleanField(default=0)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityCerti',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('certificate_type_id', models.IntegerField()),
                ('gained_date', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityDoc',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(max_length=100)),
                ('path', models.TextField(max_length=255)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('created_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityFormer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityHistory',
            fields=[
                ('commu_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('updated_date', models.DateField(auto_now_add=True)),
                ('updated_content', models.CharField(blank=True, max_length=255)),
                ('community_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('updated_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('is_mentor', models.BooleanField(default=False)),
                ('point', models.IntegerField(default=0)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Community.community')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='Member',
            field=models.ManyToManyField(related_name='groups_joined', through='Community.CommunityMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
