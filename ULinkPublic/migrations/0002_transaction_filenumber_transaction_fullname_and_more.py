# Generated by Django 4.1 on 2022-10-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULinkPublic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='fileNumber',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='fullname',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='vdxpaper',
            name='fileNumber',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='vdxpaper',
            name='fullname',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
    ]
