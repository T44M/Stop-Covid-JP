from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import environ
import os
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

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

li = ["%E9%83%BD%E5%B3%B6%E5%8C%BA", 
"%E7%A6%8F%E5%B3%B6%E5%8C%BA", 
"%E6%AD%A4%E8%8A%B1%E5%8C%BA", 
"%E8%A5%BF%E5%8C%BA", 
"%E6%B8%AF%E5%8C%BA", 
"%E5%A4%A7%E6%AD%A3%E5%8C%BA", 
"%E5%A4%A9%E7%8E%8B%E5%AF%BA%E5%8C%BA", 
"%E6%B5%AA%E9%80%9F%E5%8C%BA", 
"%E8%A5%BF%E6%B7%80%E5%B7%9D%E5%8C%BA", 
"%E6%9D%B1%E6%B7%80%E5%B7%9D%E5%8C%BA", 
"%E6%9D%B1%E6%88%90%E5%8C%BA", 
"%E7%94%9F%E9%87%8E%E5%8C%BA", 
"%E6%97%AD%E5%8C%BA", 
"%E5%9F%8E%E6%9D%B1%E5%8C%BA", 
"%E9%98%BF%E5%80%8D%E9%87%8E%E5%8C%BA", 
"%E4%BD%8F%E5%90%89%E5%8C%BA", 
"%E6%9D%B1%E4%BD%8F%E5%90%89%E5%8C%BA", 
"%E8%A5%BF%E6%88%90%E5%8C%BA", 
"%E6%B7%80%E5%B7%9D%E5%8C%BA", 
"%E9%B6%B4%E8%A6%8B%E5%8C%BA", 
"%E4%BD%8F%E4%B9%8B%E6%B1%9F%E5%8C%BA", 
"%E5%B9%B3%E9%87%8E%E5%8C%BA", 
"%E5%8C%97%E5%8C%BA", 
"%E4%B8%AD%E5%A4%AE%E5%8C%BA"]

areas = ["都島区", 
"福島区", 
"此花区", 
"西区", 
"港区", 
"大正区", 
"天王寺区", 
"浪速区", 
"西淀川区", 
"東淀川区", 
"東成区", 
"生野区", 
"旭区", 
"城東区", 
"阿倍野区", 
"住吉区", 
"東住吉区", 
"西成区", 
"淀川区", 
"鶴見区", 
"住之江区", 
"平野区", 
"北区", 
"中央区"]
totalPlaces = []
urls = []

for i in li:
    url = "https://v-sys.mhlw.go.jp/search/list.html?id=271004&availableOnly=on&generalPracticeOnly=on&keyword=" + i + "&vaccineMaker=&page=1"
    
    driver.get(url)
    urls.append(url)

    time.sleep(3)
    
    try:
        totalPlace = driver.find_element_by_xpath("//*[@id='main-content']/div[1]/div/div[6]/p").text[14:]
        totalPlaces.append(totalPlace)
    except:
        totalPlaces.append("nodata")

driver.close()

if __name__ == '__main__':
    auth = tweepy.OAuthHandler('3Gkn2Y145WwZ5kFt4NBCBKVGm', 'nio5smQQLOex29tIEJiDWlXUiE8JCi8Y6fmuzQ1DOYKt2QCKrK')
    auth.set_access_token('1355161653961228291-qHLAUQO5YNckIeln2qGn5bVK5T43AK', 'ZXVBIVxGHDLuKYJ0zMA9vbIsfmRporIqRw4790KMujNLN')

    # Create API object
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print('Authentication Successful')
    except:
        print('Error while authenticating API')
        sys.exit(1)

    for areaslist, totalPlaceslist, urlslist in zip (areas, totalPlaces, urls):

        if totalPlaceslist == "nodata":
            nodata = f"""【ワクチン接種会場】
({date})
{areaslist}には、現在、予約可能会場がありません。
            
URL: {urlslist}
            
#Covid19Vaccine #ワクチン #COVID19"""
            
            time.sleep(60)
            api.update_status(nodata)
            
        else:
            tweet1 = f"""【ワクチン接種会場】
({date})
{areaslist}にて、{totalPlaceslist}の接種会場が予約可能。

予約: {urlslist}

#Covid19Vaccine #ワクチン #COVID19"""
            
            time.sleep(60)
            api.update_status(tweet1)
    
print("All of tweet is successful")