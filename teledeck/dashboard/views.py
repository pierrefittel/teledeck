from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.serializers import json

from .forms import AddChannel
from .models import Message, Channel, Group

def index (request):
    #Retrieve all groups
    groups = Group.objects.all()
    #Retrieve all channels
    channels = Channel.objects.all()
    #Retrieve all messages
    messages = Message.objects.all()
    #Remove unselected channel from selection
    for channel in channels:
        if channel.channel_toggle == False:
            messages = messages.exclude(channel_name = channel.channel_name)
    messages = messages.order_by('-message_date')
    #Channel edit form
    form = AddChannel()
    #Message data JSON serialization for JS manipulation
    json_serializer = json.Serializer()
    messages_data = json_serializer.serialize(Message.objects.all())
    context = {'groups': groups, 'messages': messages, 'channels': channels, 'form': form, 'messages_data': messages_data}
    return render(request, 'dashboard/index.html', context)

def add_channel(request):
    if request.method == "POST":
        form = AddChannel(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = AddChannel()
    return HttpResponseRedirect('/dashboard')

def toggle_channel(request, channel_name=None):
    channel = Channel.objects.get(channel_name=channel_name)
    if channel.channel_toggle == True:
        channel.channel_toggle = False
        channel.save()
    elif channel.channel_toggle == False:
        channel.channel_toggle = True
        channel.save()
    return HttpResponseRedirect('/dashboard')

def show_detail(request, id=None):
    message = Message.objects.get(id=id)
    print(message.message_text)
    return HttpResponseRedirect('/dashboard')

def toggle_group(request, channel_group=None):
    print('test')
    channel_group = Group.objects.get(channel_group=channel_group)
    channels = Channel.objects.get(channel_group=channel_group)
    if channel_group.groupe_toggle == True:
        for channel in channels:
            channel.channel_toggle = True
            channel.save()
    elif channel_group.groupe_toggle == False:
        for channel in channels:
            channel.channel_toggle = False
            channel.save()
    return HttpResponseRedirect('/dashboard')

def delete_channel(request, channel_name=None):
    channel = Channel.objects.get(channel_name=channel_name)
    channel.delete()
    return HttpResponseRedirect('/dashboard')