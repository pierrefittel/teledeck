# Generated by Django 4.1.5 on 2023-02-03 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_message_reply_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_category',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
