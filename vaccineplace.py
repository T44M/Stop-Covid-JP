from selenium import webdriver
from os import environ
import datetime
import tweepy
import time
import sys

now = datetime.datetime.now()
date = now.strftime("%Y/%m/%d %H:%M")

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_KEY_SECRET = environ['ACCESS_KEY_SECRET']

driver = webdriver.Chrome("C:/Users/go_MT\Downloads/chromedriver_win32/chromedriver.exe")

li = ["131181", 
"131199", 
"131113", 
"131237", 
"131229", 
"131172", 
"131083", 
"131091", 
"131130", 
"131041", 
"131156", 
"131075", 
"131121", 
"131067", 
"131024", 
"131016", 
"131148", 
"131202", 
"131059", 
"131032", 
"131105"]

areas = []
totalPlaces = []
urls = []

for i in li:
    url = "https://v-sys.mhlw.go.jp/search/list.html?id=" + i + "&availableOnly=on&generalPracticeOnly=on&keyword=&vaccineMaker=&page=1"
    
    driver.get(url)
    urls.append(url)

    time.sleep(3)
    
    area = driver.find_element_by_xpath("/html/body/div[2]/main/div[1]/div/div[2]/h2").text
    areas.append(area)
    
    try:
        totalPlace = driver.find_element_by_xpath("//*[@id='main-content']/div[1]/div/div[6]/p").text[14:]
        totalPlaces.append(totalPlace)
    except:
        totalPlaces.append("nodata")

driver.close()

tweets = []

for areaslist, totalPlaceslist, urlslist in zip (areas, totalPlaces, urls):
    
    tweet = f'''【ワクチン接種会場】
    ({date})
    {areaslist}にて、{totalPlaceslist}の接種会場が予約可能。

    予約: {urlslist}

    #COVID19'''
    
    tweets.append(tweet)
    
    if totalPlaceslist == "nodata":
        nodata = f'''【ワクチン接種会場】
        ({date})
        {areaslist}には、現在、予約可能会場がありません。
        
        URL: {urlslist}
        
        #COVID19'''
        
        tweets.append(nodata)

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

    for tweetslist in zip(tweets):
        api.update_status(tweetslist)
        time.sleep(60)
        print('Tweet successful')

