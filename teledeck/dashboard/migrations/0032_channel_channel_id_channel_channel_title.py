# Generated by Django 4.1.5 on 2023-02-17 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_parameter_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='channel_title',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
