import sys
import datetime
import requests
import tweepy
from lxml import html

now = datetime.datetime.now()
date = now.strftime("%Y/%m/%d %H:%M")


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

    tweet = total_covid()
    api.update_status(tweet)
    print('Tweet successful')