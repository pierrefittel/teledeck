# Generated by Django 4.1.5 on 2023-02-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_channels_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]