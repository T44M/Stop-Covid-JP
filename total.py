import sys
import datetime
import requests
import tweepy
import time
from lxml import html
from os import environ

response = requests.get('https://news.google.com/covid19/map?hl=ja&gl=JP&ceid=JP%3Aja&mid=%2Fm%2F03_3d&state=4')
tag = html.fromstring(response.content)

now = datetime.datetime.now()
date = now.strftime("%Y/%m/%d %H:%M")

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_KEY_SECRET = environ['ACCESS_KEY_SECRET']

def news_covid():
    try:
        a, b, c, d = tag.xpath('//div[@class="UvMayb"]/text()')
        a1, b1, c1, d1 = tag.xpath('//div[@class="tIUMlb"]/strong/text()')
    
    except ValueError:
        a1, b1, d1 = tag.xpath('//div[@class="tIUMlb"]/strong/text()')

    tweet_world = f'''{date}
【新型コロナウィルス感染情報】
日本国内

新たな感染者(累計感染者)：
{a1}({a})

昨日の死亡者(累計死亡者):
{b1}({b})

ソース: https://ux.nu/uOa8V
#COVID19'''
        
    return tweet_world

def vaccine_covid():
    try:
        a, b, c, d = tag.xpath('//div[@class="UvMayb"]/text()')
        a1, b1, c1, d1 = tag.xpath('//div[@class="tIUMlb"]/strong/text()')

    except ValueError:
        a1, b1, d1 = tag.xpath('//div[@class="tIUMlb"]/strong/text()')
        tweet_world2 = f'''{date}
【新型コロナワクチン接種】
日本国内

昨日の接種数: no data
合計接種数: {c}

必要回数接種済み: {d}
人口比: {d1}

ソース: https://ux.nu/uOa8V
#COVID19'''

    else:
        tweet_world2 = f'''{date}
【新型コロナワクチン接種】
日本国内

昨日の接種数: {c1}
合計接種数: {c}

必要回数接種済み: {d}
人口比: {d1}

ソース: https://ux.nu/uOa8V
#COVID_19'''

    return tweet_world2

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_KEY_SECRET)

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print('Authentication Successful')
    except:
        print('Error while authenticating API')
        sys.exit(1)

    tweet = news_covid()
    tweet2 = vaccine_covid()
    api.update_status(tweet)
    time.sleep(60)
    api.update_status(tweet2)
    
print('Tweet successful')