from telethon import TelegramClient, utils
import sqlite3
import asyncio
from googletrans import Translator

#Parameters
API_ID = 21437350
API_HASH = '89452b63dc750b11efad4025ec484845'

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

def translateMessage(message):
    translator = Translator()
    translation = translator.translate(message, dest='fr')
    return translation

#Retrieve channel messages from each channel
async def retrieveMessage(iter):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        channels = populateChannelList()
        messages = []
        for channel in channels:
            channel_name = {"channel_name": channel}
            async for message in client.iter_messages(channel, iter):
                data = message.to_dict()
                data.update(channel_name)
                messages.append(data)
        return messages

#This module check wether a Telegram channel exists and return a boolean response
async def channelValidation(id):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        try:
            response = await client.get_entity(id)
        except ValueError:
            response = 'error'
        return response