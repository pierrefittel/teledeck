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


class Channel(models.Model):
    channel_name = models.CharField(max_length=100, unique=True)
    channel_group = models.CharField(max_length=100)
    channel_toggle = models.BooleanField()
    def __str__(self):
        return self.channel_name

class Group(models.Model):
    channel_group = models.CharField(max_length=100)
    group_toggle = models.BooleanField()
    def __str__(self):
        return self.channel_group

class Filter(models.Model):
    text_filter = models.CharField(max_length=100)
    translation_filter = models.CharField(max_length=100)
    view_count = models.IntegerField()
    share_count = models.IntegerField()
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)