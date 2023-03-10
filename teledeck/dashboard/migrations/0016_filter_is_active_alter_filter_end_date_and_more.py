# Generated by Django 4.1.5 on 2023-02-05 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_filter_share_count_filter_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filter',
            name='end_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='filter',
            name='start_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
