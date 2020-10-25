import requests
from mongohelper import *
from os import environ

def telegram_bot_sendtext(bot_message):
    
    bot_token = environ.get('bot_token')
    bot_chatID = environ.get('bot_chatid')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

    

