from django.db import models
import datetime

class Message(models.Model):
    message_id = models.IntegerField()
    message_text = models.CharField(max_length=5000)
    text_translation = models.CharField(max_length=5000)
    message_date = models.DateTimeField('date published')
    channel_name = models.CharField(max_length=100)
    view_count = models.IntegerField()
    share_count = models.IntegerField()
    def __str__(self):
        message_url = 'https://t.me/{}/{}'.format(self.channel_name, self.message_id)
        return message_url

class Channel(models.Model):
    channel_name = models.CharField(max_length=100, unique=True)
    channel_group = models.CharField(max_length=100)
    channel_toggle = models.BooleanField(default=True)
    def __str__(self):
        return self.channel_name

class Group(models.Model):
    channel_group = models.CharField(max_length=100)
    group_toggle = models.BooleanField()
    def __str__(self):
        return self.channel_group

class Filter(models.Model):
    text_filter = models.CharField(max_length=100, blank=True)
    translation_filter = models.CharField(max_length=100, blank=True)
    view_count = models.IntegerField(null=True)
    share_count = models.IntegerField(null=True)
    start_date = models.DateTimeField(default=datetime.date.today, null=True)
    end_date = models.DateTimeField(default=datetime.date.today, null=True)
    is_active = models.BooleanField(default=False)

class Parameter(models.Model):
    #Define message threat sort order (date)
    SORTING_CHOICES = (
        ('UP', 'upward'),
        ('DOWN', 'downward'),
    )
    message_sort_by_date = models.CharField(max_length=10, choices=SORTING_CHOICES)
    #Define message load number
    message_load_number = models.IntegerField()