# Generated by Django 4.1.5 on 2023-02-03 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_remove_message_channel_toggle_channel_channel_toggle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channel',
            old_name='channel_category',
            new_name='channel_group',
        ),
    ]
