from telethon import TelegramClient
from telethon import tl
import sqlite3
from datetime import datetime, timedelta
from googletrans import Translator
import os, shutil

#Retrieve channel names from config
def populateChannelList():
    channel_list = []
    connexion = sqlite3.connect('./teledeck/db.sqlite3')
    cursor = connexion.cursor()
    data = cursor.execute("SELECT * FROM dashboard_channel")
    channels = data.fetchall()
    for i in channels:
        channel_list.append(i[1])
    return channel_list

#Write data to Django DB
def writeToDB(data):
    connexion = sqlite3.connect('./teledeck/db.sqlite3')
    cursor = connexion.cursor()
    for msg in data:
        try:
            message_text = msg['message']
            text_translation = translateMessage(msg['message'])
            views = msg['views']
            shares = msg['forwards']
        except KeyError:
            message_text = 'No message available'
            text_translation.text = 'No translation available'
            views = 0
            shares = 0
        query = """REPLACE INTO dashboard_message
        (message_text, text_translation, message_date, channel_name, view_count, share_count, message_id)
        VALUES (?, ?, ?, ?, ?, ?, ?);"""
        data_tuple = (message_text, text_translation.text, msg['date'], msg['channel_name'], views, shares, msg['id'])
        cursor.execute(query, data_tuple)
        connexion.commit()
    cursor.close()

#Translate message through Google Translate API - message size limited
def translateMessage(message):
    translator = Translator()
    translation = translator.translate(message, dest='fr')
    return translation

#Retrieve channel messages from each channel
async def retrieveMessage(API_ID, API_HASH, limit):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        time_limit = datetime.today() - timedelta(days=limit)
        channels = populateChannelList()
        messages = []
        for channel in channels:
            channel_name = {"channel_name": channel}
            async for message in client.iter_messages(channel, reverse=True, offset_date=time_limit):
                data = message.to_dict()
                data.update(channel_name)
                messages.append(data)
        return messages

#Check wether a Telegram channel exists and return a boolean response
async def channelValidation(API_ID, API_HASH, id):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        try:
            response = await client.get_entity(id)
        except ValueError:
            response = 'error'
        return response

#Retrieve any media associated with a message
async def mediaDownload(API_ID, API_HASH, channel, messageID):
    directory = './teledeck/dashboard/static/dashboard/media'
    #Delete every file in media directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    #Download all medias associated to the message in the directory
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        async for message in client.iter_messages(channel, ids=messageID):
            if (type(message.media) == tl.types.MessageMediaPhoto):
                path = await message.download_media(file=directory)
                return path
            else:
                return None


