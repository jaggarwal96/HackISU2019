import urllib

import tweepy
from tweepy import OAuthHandler
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time

consumer_key = 'WCqb4vOIcppLOHxJD4Z4q2xwQ'
consumer_secret = 'kWWChyjsJjeyKZQRUSDs2qnojuBhfWBXxjz11TyfqEdMmcgjEj'
access_token = '977352389421187078-E8DkXkeTkm5GYMUQkOy3mCK9BrCLOan'
access_secret = 'ZAUXyIWPlle3q5CVXl66Lfdoc5BhmN22jHQXTEYFT3R2C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


if __name__ == '__main__':

    friends = api.friends_ids("CNBC")
    # for i in range(0, len(friends)):
    #     user = api.get_user(friends[i])
    #     print('{} {}'.format(user.screen_name,user.followers_count))

    goodUsers = []
    i = 1
    index = 0;
    for fr in friends:

        url = "https://twitter.com/intent/user?user_id=" + str(fr)
        #print(url)
        print(i)
        if(i % 100 == 0):
            print("sleeping")
            time.sleep(60)
            print("continuing")
        content = urlopen(url)

        soup = BeautifulSoup(content, 'html.parser')
        i = i + 1

        followers = ""
        verified = ""
        print(fr)
        try:
            followers = soup.find("a", href=re.compile("/followers")).string
            followers = followers.replace(",", "")
            verified = soup.find("li", class_="verified").string
            print(verified)
            # print(followers)
        except AttributeError:
            print("error")
            continue

        if(int(followers) > 100000 and verified.strip() == "Verified account"):
            handle = soup.find("span", class_="nickname").string
            handle = handle[1:]
            #print(handle)
            index = index + 1
            goodUsers.append(handle)


        if(index == 12):
            break

    print(goodUsers)



