# Generated by Django 4.1 on 2022-10-17 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULinkPublic', '0002_transaction_filenumber_transaction_fullname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='nas',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='vdxpaper',
            name='nas',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
    ]