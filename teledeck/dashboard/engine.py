from telethon import TelegramClient
from telethon import tl
from datetime import datetime, timedelta
from googletrans import Translator
import os, shutil

#Translate message through Google Translate API - message size limited
def translateMessage(message):
    translator = Translator()
    translation = translator.translate(message, dest='fr')
    return translation

#Retrieve channel messages from each channel
async def retrieveMessage(API_ID, API_HASH, limit, channel):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        time_limit = datetime.today() - timedelta(days=limit)
        messages = []
        async for message in client.iter_messages(channel, reverse=True, offset_date=time_limit):
            data = message.to_dict()
            data.update({"channel_name": channel})
            messages.append(data)
        return messages

#Check whether a Telegram channel exists and return details
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


