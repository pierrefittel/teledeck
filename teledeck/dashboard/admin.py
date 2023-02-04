from django.contrib import admin

# Register your models here.
from .models import Message, Channel, Group

admin.site.register(Message)
admin.site.register(Channel)
admin.site.register(Group)