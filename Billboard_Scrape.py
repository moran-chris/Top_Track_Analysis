import bs4  
import numpy as np 
import requests 
import pandas as pd 
import datetime 
from pymongo import MongoClient
from time import sleep

client = MongoClient('localhost',27017)
db = client['billboard_3']
table = db['hot_100']

# original page page = requests.get('https://www.billboard.com/charts/hot-100')
    #page = requests.get('https://www.billboard.com/charts/hot-100/2020-03-28')
    #soup = bs4.BeautifulSoup(page.content,'html.parser')

start_date = datetime.datetime.strptime('1958/08/23','%Y/%m/%d')
#start_date = datetime.datetime.strptime('2020/03/07','%Y/%m/%d')
end_date = datetime.datetime.strptime('2020/03/28','%Y/%m/%d')

count = 0
while start_date != end_date:
    d = {}
    page = requests.get('https://www.billboard.com/charts/hot-100/'+str(start_date.date()))
    soup = bs4.BeautifulSoup(page.content,'html.parser')
    rank = soup.find_all(class_ = 'chart-element__rank__number')
    rank = [str(x) for x in rank]
    songs = soup.find_all(class_='chart-element__information__song text--truncate color--primary')
    songs = [str(x) for x in songs]
    artist = soup.find_all(class_="chart-element__information__artist text--truncate color--secondary")
    artist = [str(x) for x in artist]
    previous_week = soup.find_all(class_='chart-element__meta text--center color--secondary text--last')
    previous_week = [str(x) for x in previous_week]
    peak = soup.find_all(class_='chart-element__meta text--center color--secondary text--peak')
    peak = [str(x) for x in peak]
    duration = soup.find_all(class_='chart-element__meta text--center color--secondary text--week')
    duration = [str(x) for x in duration]
    d = {'date':str(start_date.date()),'rank': rank, 'songs': songs, 'artist':artist, 'previous_week': previous_week,'peak': peak, 'duration':duration}
    start_date = start_date + datetime.timedelta(days=7)
    table.insert_one(d)
    count += 1
    sleep(2)
    print(count)

