# Generated by Django 4.1.5 on 2023-02-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_message_channel_toggle_alter_channel_channel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='channel_toggle',
        ),
        migrations.AddField(
            model_name='channel',
            name='channel_toggle',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
