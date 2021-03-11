import sys
import datetime
import requests
import tweepy
import os
from lxml import html
from os import environ

now = datetime.datetime.now()
date = now.strftime("%Y/%m/%d %H:%M")

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_KEY_SECRET = environ['ACCESS_KEY_SECRET']

def total_covid():
    response = requests.get('https://www.worldometers.info/coronavirus/')
    doc = html.fromstring(response.content)
    total, deaths, recovered = doc.xpath('//div[@class="maincounter-number"]/span/text()')

    responsejp = requests.get('https://www.worldometers.info/coronavirus/country/japan/')
    docjp = html.fromstring(responsejp.content)
    totalj, deathsj, recoveredj = docjp.xpath('//div[@class="maincounter-number"]/span/text()')

    tweet_world = f'''【新型コロナ感染者数】
日本
   -感染者: {totalj}
   -回復者: {recoveredj}
   -死亡者: {deathsj}
世界
   -全世界累計: {total}
   -全回復累計: {recovered}
   -全死亡累計: {deaths} 
ソース: https://bit.ly/2SIVKY6
#COVID19
取得 {date}'''
            
    return tweet_world

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print('Authentication Successful')
    except:
        print('Error while authenticating API')
        sys.exit(1)

    tweet = total_covid()
    api.update_status(tweet)
    print('Tweet successful')
