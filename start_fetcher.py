from Ingestion.fetcher import *

data = getListings()
if not len(data) > 0:
    raise Exception(f'Unable to fetch listings information from page: {URL}')
storeData(data)
