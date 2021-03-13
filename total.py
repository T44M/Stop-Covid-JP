import sys
import datetime
import requests
import tweepy
import time
from lxml import html

response = requests.get('https://news.google.com/covid19/map?hl=ja&gl=JP&ceid=JP%3Aja&mid=%2Fm%2F03_3d&state=4')
tag = html.fromstring(response.content)

now = datetime.datetime.now()
date = now.strftime("%Y/%m/%d %H:%M")

def news_covid():
    a, b, c, d = tag.xpath('//div[@class="UvMayb"]/text()')
    a1, b1, c1, d1 = tag.xpath('//div[@class="tIUMlb"]/strong/text()')
    tweet_world = f'''【新型コロナウィルス感染情報】
日本国内

新たな感染者(累計感染者)：
{a1}({a})

昨日の死亡者(累計死亡者):
{b1}({b})

ソース: https://ux.nu/uOa8V
#COVID19
取得 {date}'''
        
    return tweet_world

def vaccine_covid():
    a, b, c, d = tag.xpath('//div[@class="UvMayb"]/text()')
    a1, b1, c1, d1 = tag.xpath('//div[@class="tIUMlb"]/strong/text()')
    tweet_world2 = f'''【新型コロナワクチン接種】
日本国内

昨日の接種数: {c1}
合計接種数: {c}

必要回数接種済み: {d}
人口比: {d1}

ソース: https://ux.nu/uOa8V
#COVID19
取得 {date}'''

    return tweet_world2

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

    tweet = news_covid()
    tweet2 = vaccine_covid()
    api.update_status(tweet)
    time.sleep(35)
    api.update_status(tweet2)
    print('Tweet successful')