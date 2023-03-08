from telethon import TelegramClient
from telethon import tl
from datetime import datetime, timedelta
from googletrans import Translator
import os, shutil

def translateMessage(message):
    #Translate message through Google Translate API - message size limited
    translator = Translator()
    translation = translator.translate(message, dest='fr')
    return translation

async def retrieveMessage(API_ID, API_HASH, limit, channel):
    #Retrieve channel messages from each channel
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        time_limit = datetime.today() - timedelta(days=limit)
        messages = []
        async for message in client.iter_messages(channel, reverse=True, offset_date=time_limit):
            data = message.to_dict()
            data.update({"channel_name": channel})
            messages.append(data)
        return messages

async def channelValidation(API_ID, API_HASH, id):
    #Check whether a Telegram channel exists and return details
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        try:
            response = await client.get_entity(id)
        except ValueError:
            response = 'error'
        return response

async def mediaDownload(API_ID, API_HASH, channel, messageID):
    #Retrieve any media associated with a message
    directory = './dashboard/static/dashboard/media'
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

async def sendCodeRequest(API_ID, API_HASH, phone_number, password):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        if client.is_connected() == True:
            return client.is_connected()
        elif client.is_connected() == False:
            await client.start(phone_number, password)
    

async def sendCode(API_ID, API_HASH, phone_number, code):
    #Not used
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.sign_in(phone_number, code)