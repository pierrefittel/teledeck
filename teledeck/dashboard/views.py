import csv
import asyncio
import pandas
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers import json
from django.db.models.functions import Lower

from .engine import writeToDB, retrieveMessage, channelValidation
from .forms import AddChannel, CreateFilter
from .models import Message, Channel, Group, Filter, Parameter

def index(request):
    #Retrieve all groups
    groups = Group.objects.all().order_by('channel_group')
    #Retrieve all channels
    channels = Channel.objects.all().order_by(Lower('channel_name'))
    #Retrieve all messages
    messages = filter_messages(request, "view")
    #Retrieve all filters
    filters = Filter.objects.all()
    #Retrieve all parameters
    parameters = Parameter.objects.get(user_name='admin')
    #Channel edit form
    add_channel = AddChannel()
    #Filter form
    create_filter = CreateFilter()
    #Message data JSON serialization for JS manipulation
    json_serializer = json.Serializer()
    messages_data = json_serializer.serialize(Message.objects.all())
    context = {
        'groups': groups,
        'messages': messages,
        'channels': channels,
        'filters': filters,
        'add_channel': add_channel,
        'create_filter': create_filter,
        'messages_data': messages_data,
        'parameters': parameters,
        }
    return render(request, 'dashboard/index.html', context)

def update_data(request):
    limit = Parameter.objects.get(user_name='admin').message_retrieve_limit
    data = asyncio.run(retrieveMessage(limit))
    writeToDB(data)
    messages = filter_messages(request, "view")
    context = {'messages': messages}
    return render(request, 'dashboard/messages.html', context)

def toggle_group(request, channel_group=None):
    channel_group = Group.objects.get(channel_group=channel_group)
    channels = Channel.objects.filter(channel_group=channel_group)
    if channel_group.group_toggle == True:
        channel_group.group_toggle = False
        channel_group.save()
        for channel in channels:
            channel.channel_toggle = False
            channel.save()
    elif channel_group.group_toggle == False:
        channel_group.group_toggle = True
        channel_group.save()
        for channel in channels:
            channel.channel_toggle = True
            channel.save()
    groups = Group.objects.all().order_by('channel_group')
    channels = Channel.objects.all().order_by(Lower('channel_name'))
    context = {'groups': groups, 'channels': channels}
    return render(request, 'dashboard/sources.html', context)

def toggle_channel(request, channel_name=None):
    channel = Channel.objects.get(channel_name=channel_name)
    if channel.channel_toggle == True:
        channel.channel_toggle = False
        channel.save()
    elif channel.channel_toggle == False:
        channel.channel_toggle = True
        channel.save()
    groups = Group.objects.all().order_by('channel_group')
    channels = Channel.objects.all().order_by(Lower('channel_name'))
    context = {'groups': groups, 'channels': channels}
    return render(request, 'dashboard/sources.html', context)

def add_channel(request):
    if request.method == "POST":
        channel_name = request.POST['channel_name']
        response = asyncio.run(channelValidation(channel_name))
        if response != 'error':
            form = AddChannel(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard')
    else:
        form = AddChannel()
    return HttpResponseRedirect('/dashboard')

def delete_channel(request, channel_name=None):
    channel = Channel.objects.get(channel_name=channel_name)
    channel.delete()
    groups = Group.objects.all().order_by('channel_group')
    channels = Channel.objects.all().order_by(Lower('channel_name'))
    context = {'groups': groups, 'channels': channels}
    return render(request, 'dashboard/sources.html', context)

def create_filter(request):
    if request.method == "POST":
        form = CreateFilter(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = CreateFilter()
    return HttpResponseRedirect('/dashboard')

def toggle_filter(request, filter_id=None):
    filter = Filter.objects.get(pk=filter_id)
    if filter.is_active == True:
        filter.is_active = False
        filter.save()
    elif filter.is_active == False:
        filter.is_active = True
        filter.save()
    filters = Filter.objects.all()
    context = {'filters': filters}
    return render(request, 'dashboard/filter.html', context)

def delete_filter(request, filter_id=None):
    filter = Filter.objects.get(pk=filter_id)
    filter.delete()
    filters = Filter.objects.all()
    context = {'filters': filters}
    return render(request, 'dashboard/filter.html', context)

def filter_messages(request, caller=None):
    channels = Channel.objects.all()
    filters = Filter.objects.all()
    messages = Message.objects.all()
    #Filter messages from sources
    for channel in channels:
        if channel.channel_toggle == False:
            messages = messages.exclude(channel_name = channel.channel_name)
    #Filter messages from filters
    for filter in filters:
        if filter.is_active == True:
            if filter.text_filter != None:
                #Filter messages from text
                messages = messages.filter(message_text__icontains = filter.text_filter)
            if filter.translation_filter != None:
                #Filter messages from translation
                messages = messages.filter(text_translation__icontains = filter.translation_filter)
            if filter.view_count != None:
                #Filter messages from views
                messages = messages.filter(view_count__gte = filter.view_count)
            if filter.share_count != None:
                #Filter messages from shares
                messages = messages.filter(share_count__gte = filter.share_count)
            if filter.start_date != None:
                #Filter messages from start date
                messages = messages.filter(message_date__gte = filter.start_date)
            if filter.end_date != None:
                #Filter messages from end date
                messages = messages.filter(message_date__lte = filter.end_date)
    #Sort by date upward or downward based on account parameter
    parameters = Parameter.objects.get(user_name='admin')
    if parameters.message_sort_by_date == 'UP':
        if request.get_full_path() == '/dashboard/sort-by-date':
            #Prevent parameter modification on page reload
            messages = messages.order_by('-message_date')
            parameters.message_sort_by_date = 'DOWN'
            parameters.save()
        else:
            messages = messages.order_by('message_date')
    elif parameters.message_sort_by_date == 'DOWN':
        if request.get_full_path() == '/dashboard/sort-by-date':
            #Prevent parameter modification on page reload
            messages = messages.order_by('message_date')
            parameters.message_sort_by_date = 'UP'
            parameters.save()
        else:
            messages = messages.order_by('-message_date')
    #Render filtered messages and return them to another function or request depending on caller
    context = {'messages': messages, 'parameters': parameters}
    if caller == 'view':
        #If caller is another view, return messages as an object
        return messages
    else:
        #If caller is a GET request, return messages as a segment of a webpage
        return render(request, 'dashboard/messages.html', context)

def export_CSV(request):
    if request.method == "POST":
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="export.csv"'},
        )
        messages = filter_messages(request, "view")
        writer = csv.writer(response)
        writer.writerow(['ID', 'Channel', 'Message ID', 'Message text', 'Message translation', 'Date', 'Views', 'Shares', 'URL'])
        for message in messages:
            message_url = 'https://t.me/{}/{}'.format(message.channel_name, message.message_id)
            writer.writerow([message.pk, message.channel_name, message.message_id, message.message_text, message.text_translation, message.message_date, message.view_count, message.share_count, message_url])
    return response

def get_data(request):
    if request.method == "GET":
        messages = filter_messages(request, "view")
        json_serializer = json.Serializer()
        content = json_serializer.serialize(messages)
        response = HttpResponse(
            content,
            content_type='application/json',
            headers={'Content-Disposition': 'inline'},
        )
    return response
