# Generated by Django 5.0.4 on 2024-06-01 05:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0010_alter_myuser_userid_alter_usercommunity_user_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommunity',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_community', to=settings.AUTH_USER_MODEL),
        ),
    ]