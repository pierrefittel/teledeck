# Generated by Django 4.1.5 on 2023-02-01 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_message_reply_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.CharField(max_length=100),
        ),
    ]
