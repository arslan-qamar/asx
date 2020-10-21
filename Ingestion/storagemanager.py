from mongohelper import *
from datetime import datetime

COLLECTION_NAME = 'listings'

def storeData(data):
    collection = getMongoCollection(COLLECTION_NAME)
    for d in data:
        post_data = {
            'Rank': d[0],
            '_id': d[2],
            'Code': d[2],
            'Company': d[3],
            'Price': d[4],
            'Change': d[5],
            'Percentage_Change': d[6],
            'Market_Cap': d[7],
            'Year_Percentage_Change': d[8]
            }
           
        collection.update(post_data,
            {
            "$setOnInsert": {"Discovered_At": datetime.utcnow()},
            "$set": {"Last_Updated_On": datetime.utcnow()},
            },
            True)