import requests
from bs4 import BeautifulSoup
from os import environ
import pymongo
from pymongo import MongoClient
from datetime import datetime

URL = 'https://www.marketindex.com.au/asx-listed-companies'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
DATABASE_NAME = 'asx'
COLLECTION_NAME = 'listings'

def getSession():
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    return session

def getPageData(url):
    session = getSession()
    page = session.get(URL).text
    return page

def getListings():
    html = getPageData(URL)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='asx_sp_table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data

def getMongoClient():
    if environ.get('asx_db') is None:
        raise Exception('Please set asx_db connection value for mongodb.')
    return MongoClient(environ.get('asx_db'))

def getMongoDB(databaseName):
    return getMongoClient()[DATABASE_NAME]

def getMongoCollection(databaseName, collectionName):
    return getMongoDB(databaseName)[collectionName]

def storeData(data):
    collection = getMongoCollection(DATABASE_NAME, COLLECTION_NAME)
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

data = getListings()
success = storeData(data)
