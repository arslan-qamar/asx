import requests
from mongohelper import *
from os import environ
import telegram

def telegram_bot_sendtext(bot_message):
    
    bot_token = environ.get('bot_token')
    bot_chatid = environ.get('bot_chatid')

    bot = telegram.Bot(token=bot_token)

    response = bot.send_message(chat_id=bot_chatid, text=bot_message, parse_mode=telegram.ParseMode.HTML)

    return response

    


