import urllib.request

def channel_validation(channel_name):
    #This module check wether a Telegram channel exists and return a boolean response
    channel_url = 'https://t.me/{}/'.format(channel_name)
    with urllib.request.urlopen(channel_url) as response:
        return response.status