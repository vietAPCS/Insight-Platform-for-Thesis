# Generated by Django 5.0.3 on 2024-06-11 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0013_rename_walletadress_myuser_walletaddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='WalletAddress',
            new_name='metamaskID',
        ),
    ]
