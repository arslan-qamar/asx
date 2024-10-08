from mongohelper import *
from datetime import datetime
from pymongo import UpdateOne

COLLECTION_NAME = 'listings'

def storeData(data):
    collection = getMongoCollection(COLLECTION_NAME)

    ops = []
    for d in data:
        filter = {
            '_id': d[2]
            }
            
        upsert_data = {
                'Rank': d[0],
                '_id': d[2],
                'Code': d[2],
                'Company': d[3],
                'Price': d[4],
                'Change': d[5],
                'Percentage_Change': d[6],
                'Market_Cap': d[7],
                'Year_Percentage_Change': d[8],
                'Last_Updated_On': datetime.utcnow()
                }       

        ops.append(UpdateOne(filter,
            {
                "$set": upsert_data,
                "$setOnInsert": { "Discovered_At": datetime.utcnow() }
            },
            True))

        print(upsert_data)        
    
    collection.bulk_write(ops)
        
def getNewListings(startDate):
    collection = getMongoCollection(COLLECTION_NAME)

    results = collection.find({'Discovered_At' : {'$gte' : startDate}})
    return results

