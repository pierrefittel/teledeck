import csv
import asyncio
import json as JSON
import ntpath

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.serializers import json
from django.db.models.functions import Lower
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.postgres.search import SearchVector

from .engine import translateMessage, retrieveMessage, channelValidation, mediaDownload, sendCodeRequest
from .forms import UserLogin, AddChannel, CreateFilter, UserParameters
from .models import Message, Channel, Group, Filter, Parameter


def login(request):
    if request.method == "POST":
        request_content = JSON.loads(request.body)
        username = request_content['username']
        password = request_content['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return redirect('index')
        else:
            return HttpResponseBadRequest(status=405)
    elif request.method == "GET":
        #Load login page
        login_form = UserLogin()
        context = {
            'login_form': login_form
        }
        return render(request, 'dashboard/login.html', context)

def index(request):
    try:
        if request.user != None:
            #Logged in user
            current_user = request.user
            #Retrieve all parameters
            parameters = Parameter.objects.get(user_name=current_user)
            #Retrieve all groups
            groups = Group.objects.all().order_by('channel_group')
            #Retrieve all channels
            channels = Channel.objects.all().order_by(Lower('channel_name'))
            #Retrieve all messages
            messages = filter_messages(request, "view")
            #Retrieve all filters
            filters = Filter.objects.all()
            #Channel edit form
            add_channel = AddChannel()
            #Filter form
            create_filter = CreateFilter()
            context = {
                'user': current_user,
                'groups': groups,
                'messages': messages,
                'channels': channels,
                'filters': filters,
                'add_channel': add_channel,
                'create_filter': create_filter,
                'parameters': parameters,
                }
            return render(request, 'dashboard/index.html', context)
    except:
        return render(request, 'dashboard/403.html')

def check_API_auth(request):
    current_user = request.user
    parameters = Parameter.objects.get(user_name=current_user)
    content = asyncio.run(sendCodeRequest(parameters.api_id, parameters.api_hash, parameters.user_phone))
    response = HttpResponse(
            content,
            content_type='application/json',
            headers={'Content-Disposition': 'inline'},
        )
    return response

def update_data(request):
    #Remove double entries if any
    entries = Message.objects.all()
    for entry in entries:
        query = entries.filter(channel_name__exact=entry.channel_name, message_id__exact=entry.message_id)
        if len(query) > 1:
            print(query)
            for q in query[1:]:
                q.delete()
    current_user = request.user
    parameters = Parameter.objects.get(user_name=current_user)
    channels = Channel.objects.all()
    for channel in channels:
        messages = asyncio.run(retrieveMessage(parameters.api_id, parameters.api_hash, parameters.message_retrieve_limit, channel.channel_name))
        for m in messages:
            print(m['channel_name'], m['id'])
            message = Message()
            message.channel_name = m['channel_name']
            message.message_id = m['id']
            try:
                message.message_text = m['message']
            except KeyError:
                message.message_text = 'No message available'
            message.message_date = m['date']
            try:
                message.view_count = m['views']
            except KeyError:
                message.view_count = 0
            try:
                message.share_count = m['forwards']
            except KeyError:
                message.share_count = 0
            #Check if message exists, create a new entry or update an existing one
            try:
                entry = Message.objects.get(channel_name = message.channel_name, message_id = message.message_id)
                entry.view_count = message.view_count
                entry.share_count = message.share_count
                entry.save()
            except entry.DoesNotExist:
                try:
                    text_translation = translateMessage(message.message_text)
                    m.update({"text_translation": text_translation.text})
                    message.text_translation = m['text_translation']
                    message.save()
                except IntegrityError:
                    pass

    messages = filter_messages(request, "view")
    context = {'messages': messages}
    return render(request, 'dashboard/messages.html', context)

def settings(request):
    if request.method == 'GET':
        current_user = request.user
        parameters = Parameter.objects.get(user_name=current_user)
        settings_form = UserParameters(initial={
            'user_picture': parameters.user_picture,
            'user_phone': parameters.user_phone,
            'message_retrieve_limit': parameters.message_retrieve_limit,
            'message_load_number': parameters.message_load_number,
            'api_id': parameters.api_id,
            'api_hash': parameters.api_hash
            })
        context = {
                'settings_form': settings_form,
                'parameters': parameters,
                'user': current_user
            }
        return render(request, 'dashboard/settings.html', context)
    elif request.method == 'POST':
        current_user = request.user
        user = Parameter.objects.get(user_name=current_user.username)
        user_parameters = UserParameters(request.POST, instance=user)
        if user_parameters.is_valid():
            user_parameters.save()
            return redirect('index')

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

def add_channel(request):
    current_user = request.user
    parameters = Parameter.objects.get(user_name=current_user)
    if request.method == "POST":
        request_content = JSON.loads(request.body)
        channel_name = request_content['channel_name']
        channel_group = request_content['channel_group']
        response = asyncio.run(channelValidation(parameters.api_id, parameters.api_hash, channel_name))
        if response != 'error' and response.restricted != True:
            #Check if entity name is valid and if entity is public
            data = {
                'channel_id': response.id,
                'channel_name': '{}'.format(channel_name),
                'channel_title': '{}'.format(response.title),
                'channel_group': '{}'.format(channel_group)
            }
            form = AddChannel(data)
            if form.is_valid():                
                form.save()
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
    channels = Channel.objects.filter(channel_group = channel.channel_group).order_by(Lower('channel_name'))
    context = {'channels': channels}
    return render(request, 'dashboard/group.html', context)

def delete_channel(request, channel_name=None):
    channel = Channel.objects.get(channel_name=channel_name)
    channel.delete()
    channels = Channel.objects.filter(channel_group = channel.channel_group).order_by(Lower('channel_name'))
    context = {'channels': channels}
    return render(request, 'dashboard/group.html', context)

def create_filter(request):
    if request.method == "POST":
        request_content = JSON.loads(request.body)
        filter_name = request_content['filter_name']
        text_filter = request_content['text_filter']
        translation_filter = request_content['translation_filter']
        view_count = request_content['view_count']
        share_count = request_content['share_count']
        start_date = request_content['start_date']
        end_date = request_content['end_date']
        data = {
            'filter_name': '{}'.format(filter_name),
            'text_filter': '{}'.format(text_filter),
            'translation_filter': '{}'.format(translation_filter),
            'view_count': '{}'.format(view_count),
            'share_count': '{}'.format(share_count),
            'start_date': '{}'.format(start_date),
            'end_date': '{}'.format(end_date)
        }
        form = CreateFilter(data)
        if form.is_valid():                
            form.save()
    filters = Filter.objects.all()
    context = {'filters': filters}
    return render(request, 'dashboard/filter.html', context)

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
            if filter.text_filter:
                #Filter messages from text
                messages = messages.filter(message_text__icontains = filter.text_filter)
            if filter.translation_filter:
                #Filter messages from translation
                messages = messages.annotate(search=SearchVector('text_translation'),).filter(search=filter.translation_filter)
            if filter.view_count:
                #Filter messages from views
                messages = messages.filter(view_count__gte = filter.view_count)
            if filter.share_count:
                #Filter messages from shares
                messages = messages.filter(share_count__gte = filter.share_count)
            if filter.start_date:
                #Filter messages from start date
                messages = messages.filter(message_date__gte = filter.start_date)
            if filter.end_date:
                #Filter messages from end date
                messages = messages.filter(message_date__lte = filter.end_date)
    #Sort by date upward or downward based on account parameter
    current_user = request.user
    parameters = Parameter.objects.get(user_name=current_user)
    if parameters.message_sort_by_date == 'UP':
        if request.get_full_path() == '/dashboard/sort-by-date':
            #Prevent parameter modification on page reload
            messages = messages.order_by('-message_date')[:parameters.message_load_number]
            parameters.message_sort_by_date = 'DOWN'
            parameters.save()
        else:
            messages = messages.order_by('message_date')[:parameters.message_load_number]
    elif parameters.message_sort_by_date == 'DOWN':
        if request.get_full_path() == '/dashboard/sort-by-date':
            #Prevent parameter modification on page reload
            messages = messages.order_by('message_date')[:parameters.message_load_number]
            parameters.message_sort_by_date = 'UP'
            parameters.save()
        else:
            messages = messages.order_by('-message_date')[:parameters.message_load_number]
    #Render filtered messages and return them to another function or request depending on caller
    if caller == 'view':
        #If caller is another view, return messages as an object
        return messages
    else:
        #If caller is a GET request, return messages as a segment of a webpage
        context = {'messages': messages, 'parameters': parameters}
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

def get_message_detail(request, message_id=None):
    current_user = request.user
    parameters = Parameter.objects.get(user_name=current_user)
    message = Message.objects.get(pk=message_id)
    media = asyncio.run(mediaDownload(parameters.api_id, parameters.api_hash, message.channel_name, message.message_id))
    if media:
        media = 'dashboard/media/{}'.format(ntpath.basename(media))
        context = {'message': message, 'media': media}
        return  render(request, 'dashboard/detail.html', context)
    else:
        context = {'message': message}
        return  render(request, 'dashboard/detail.html', context)

def get_data(request, caller='view'):
    #Return a dataset for the quantitative analysis module
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

def sign_out(request):
    if request.method == "GET":
        current_user = request.user
        if current_user is not None:
            dj_logout(request)
            return redirect('login')
        else:
            return redirect('index')