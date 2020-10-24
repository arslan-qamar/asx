import requests
from mongohelper import *

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1398043950:AAG20P_o3Z0hgssyrGK-4gPgTG-guiCTjAQ'
    bot_chatID = '1185242210'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

    

test = telegram_bot_sendtext("Testing Telegram bot")
print(test)