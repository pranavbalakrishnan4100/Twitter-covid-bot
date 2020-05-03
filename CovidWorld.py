import tweepy
from datetime import datetime
from bs4 import BeautifulSoup as soup
import urllib.request
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

consumer_key="f2DMdPNOfrqLDQamf6JJPkEne"
consumer_secret="wZNoxWWDHzgDBm9MVQ7ppe8fjxoz0K1R1qD3D0FT9BZLkfpg1R"
access_token="1223514844655058944-I5o95ystX9S4ndFCFvb6Nc8alA954g"
access_secret="EK8mdFT2bc8UUO50KniJhe5VOoAk1RwVqCHKRFbqrChgu"

#Authentication
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api=tweepy.API(auth)

#Follow all followers
def followback(api):
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            try:
                follower.follow()
            except Exception as e:
                print("Account blocked.")
    print("Following done.")

def scrape_web():
    url='https://www.worldometers.info/coronavirus/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    request=urllib.request.Request(url=url,headers=headers)
    response=urllib.request.urlopen(request)
    page_html=response.read()
    response.close()
    page_soup=soup(page_html,"html.parser")

    containers=page_soup.findAll("div",{"id":"maincounter-wrap"})
    #print(len(containers))

    container=containers[0]

    #total cases
    totcase=container.findAll("div",{"class":"maincounter-number"})
    #print(totcase[0].text)

    container=containers[1]
    #total deaths
    totreco=container.findAll("div",{"class":"maincounter-number"})
    #print(totdeaths[0].text)

    container=containers[2]
    #total recovered
    totdeaths=container.findAll("div",{"class":"maincounter-number"})
    #print(totreco[0].text)

    tweetmessage(totcase[0].text,totdeaths[0].text,totreco[0].text)


def tweetmessage(a,b,c):
    now=datetime.now()
    moment=now.strftime("%B %d, %Y %H:%M")
    api.update_status("#COVID19 cases worldwide🌎 as of "+moment+":\nActive cases:\b"+a+"\nRecovered:\b"+b+"\nDeaths:\b"+c+" \n#CoronaVirus #StayHome ")
    print("Tweet done.")                                                                 


def searchandlike(keyword):
    user=api.me()
    phrase="Hi.I tweet live #COVID19 updates and stats regularly.Follow me @CovidBotLIVE to stay updated about the corona virus.\n #Coronavirus #stayhome"
    for tweet in api.search(q=keyword, lang="en", rpp=5):
        if (tweet.in_reply_to_status_id is not None or tweet.user.id == user.id):
            return
	
        if not tweet.favorited:
            try:
                tweet.favorite()
                """   tweetId=tweet.user.id
                username=tweet.user.screen_name
                api.update_status(""+phrase,in_reply_to_status_id=tweetId,auto_populate_reply_metadata=True)"""
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        else:
            return
        
    print("Search and like done.")

    
"""
def searchandreply(search):
    user=api.me()
    phrase="Hi.I tweet live #COVID19 updates and stats regularly.Follow me @CovidBotLIVE to stay updated about the corona virus.\n #Coronavirus #stayhome"
    for tweet in tweepy.Cursor(api.search,search).items(10):
        if (tweet.in_reply_to_status_id is not None or tweet.user.id == user.id):
            return
        else:
            try:
                tweetId=tweet.user.id
                username=tweet.user.screen_name
                api.update_status(""+phrase,in_reply_to_status_id=tweetId,auto_populate_reply_metadata=True)
                
                
            except tweepy.TweepError as e:
                 print(e.reason)
        
    print("Search and reply done.")  """  


def searchandreply():
    mentions=api.mentions_timeline(1)
    for twt in mentions:
        try:
            tweetId=twt.user.id
            print(tweetId)
            username=twt.user.screen_name
            print(username)
            phrase="Hi.I tweet live #COVID19 updates and stats regularly.Follow me @CovidBotLIVE to stay updated about the corona virus.\n #Coronavirus #stayhome"
            phrase2="Hello there, "
            api.update_status(""+phrase2+"@"+username,in_reply_to_status_id=tweetId,auto_populate_reply_metadata=True)
        except tweepy.TweepError as e:
            searchandreply()
            
since_id=1
def reply_mentions():
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():
        try:
            new_since_id=since_id
            now=datetime.now()
            moment=now.strftime("%B %d, %Y %H:%M")
            tweetName=tweet.user.screen_name
            tweetId=tweet.user.id
            new_since_id=max(tweet.id,new_since_id)
            api.update_status("Hello. @"+str(tweetName)+" "+moment,in_reply_status_id=tweet.id,auto_populate_reply_metadata=True)
        except tweepy.TweepError as e:
            if e.api_code== 187:
                print("Duplicate")
            else:
                raise e

            
followback(api)
scrape_web()

#keylist=["Corona","Covid","Covid19","Corona Virus","Quarantine","China","#StayHome"]
#for i in range(0,len(keylist)):
#searchandreply(".@CovidBotLIVE")


