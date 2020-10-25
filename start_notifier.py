from Notifier.notifier import *
from datetime import datetime

test = telegram_bot_sendtext(f"Testing Telegram bot at : {datetime.utcnow()}")
print(test)