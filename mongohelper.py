import pymongo
from pymongo import MongoClient
from os import environ

def getMongoClient():
    if environ.get('asx_db') is None:
        raise Exception('Please set asx_db connection value for mongodb.')
    return MongoClient(environ.get('asx_db'))

def getMongoDB():
    return getMongoClient().get_database()

def getMongoCollection(collectionName):
    return getMongoDB()[collectionName]