import requests
from bs4 import BeautifulSoup
from storage.storagemanager import *

URL = 'https://www.marketindex.com.au/asx-listed-companies'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'

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


