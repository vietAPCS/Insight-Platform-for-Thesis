# Generated by Django 5.0.3 on 2024-06-07 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0010_alter_myuser_userid_alter_usercommunity_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='WalletAdress',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
