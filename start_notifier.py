from Notifier.notifier import *
from datetime import datetime
from mongohelper import *
from storage.storagemanager import *
import urllib.parse



new_listings = getNewListings(datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))

for new_listing in new_listings:

    message =  f"""
    New Asx Listing : <b>{new_listing['Code']}</b>    
    Company : <b>{new_listing['Company']}</b> 
    Price : <b>{new_listing['Price']}</b> 
    Market Cap : <b>{new_listing['Market_Cap']}</b>    
    Discovered at : {new_listing['Discovered_At'].strftime('%d %b %Y %H:%M %p')}      
    Percentage Change : {new_listing['Percentage_Change']} 
    Rank : {new_listing['Rank']} 
    Year Percentage Change : {new_listing['Year_Percentage_Change']}     
    """
    msg_sent = telegram_bot_sendtext(message)
    print(msg_sent)