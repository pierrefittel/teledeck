# Generated by Django 4.1.5 on 2023-02-18 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_alter_channel_channel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channel_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]