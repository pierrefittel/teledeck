from telethon import TelegramClient
import sqlite3
from googletrans import Translator

#Retrieve channel names from config
def populateChannelList():
    channel_list = []
    connexion = sqlite3.connect('../teledeck/db.sqlite3')
    cursor = connexion.cursor()
    data = cursor.execute("SELECT * FROM dashboard_channel")
    channels = data.fetchall()
    for i in channels:
        channel_list.append(i[1])
    return channel_list

#Write data to Django DB
def writeToDB(messages):
    connexion = sqlite3.connect('../teledeck/db.sqlite3')
    cursor = connexion.cursor()
    for msg in messages:
        text_translation = translateMessage(msg['message'])
        query = """INSERT OR REPLACE INTO dashboard_message
        (message_text, text_translation, message_date, channel_name, view_count, share_count, message_id)
        VALUES (?, ?, ?, ?, ?, ?, ?);"""
        data_tuple = (msg['message'], text_translation.text, msg['date'], msg['channel_name'], msg['views'], msg['forwards'], msg['id'])
        cursor.execute(query, data_tuple)
        connexion.commit()
    cursor.close()

def translateMessage(message):
    translator = Translator()
    translation = translator.translate(message, dest='fr')
    return translation

#Retrieve channel messages from each channel
async def retrieveChnlMsg(channel_list, iter):
    messages = []
    for channel in channel_list:
        channel_name = {"channel_name": channel}
        async for message in client.iter_messages(channel, iter):
            data = message.to_dict()
            data.update(channel_name)
            messages.append(data)
    return messages

#Main sequence
api_id = 21437350
api_hash = '89452b63dc750b11efad4025ec484845'
client = TelegramClient('anon', api_id, api_hash)
iter = 10
channels = populateChannelList()

with client:
    data = []
    data = client.loop.run_until_complete(retrieveChnlMsg(channels, iter))
    writeToDB(data)