
import tweepy
from tweepy import OAuthHandler
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
import tweets_scrapper
import heapq
import psycopg2

consumer_key = 'WCqb4vOIcppLOHxJD4Z4q2xwQ'
consumer_secret = 'kWWChyjsJjeyKZQRUSDs2qnojuBhfWBXxjz11TyfqEdMmcgjEj'
access_token = '977352389421187078-E8DkXkeTkm5GYMUQkOy3mCK9BrCLOan'
access_secret = 'ZAUXyIWPlle3q5CVXl66Lfdoc5BhmN22jHQXTEYFT3R2C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
conn = psycopg2.connect(database="hack-isu", user="postgres", password="twitterbot1", host="35.232.221.83", port="5432")

api = tweepy.API(auth)

visitHandles = set()

companies = {
    "Microsoft" : "MSFT",
    "Tesla" : "TSLA",
    "Apple" : "AAPL",
    "Netflix" : "NFLX",
    "Amazon" : "AMZN",
    "Alphabet" : "GOOG",
    "Google" : "GOOG",
    "Facebook" : "FB",
    "Cisco" : "CSCO",
    "Coca Cola" : "KO",
    "Coke" : "KO",
    "Johnson & Johnson": "JNJ",
    "Exxon Mobil" : "XOM",
    "Walmart" : "WMT",
    "AT&T" : "T",
    "Home Depot" : "HD",
    "Walt Disney" : "DIS",
    "Disney" : "DIS",
    "Comcast" : "CMCSA",
    "Philip Morris" : "PM",
    "AbbVie" : "ABBV",
    "McDonald's" : "MCD",
    "McDonalds" : "MCD",
    "Nike" : "NKE",
    "Twitter" : "TWTR",
    "Union Pacific" : "UNP",
    "General Electric" : "GE",
    "GE": "GE",
    "Rockwell Collins" : "COL",
    "John Deere" : "DE",
    "UnitedHealth Group" : "UNH",
    "Optum" : "UNH",
    "Cerner" : "CERN",
    "Principal Financial" : "PFG",
    "AMD" : "AMD",
    "Advanced Micro Devices" : "AMD",
    "Bank of America" : "BAC",
    "Micron" : "MU",
    "Alibaba" : "BABA",
    "Intel" : "INTC",
    "Wells Fargo" : "WFC",
    "Oracle" : "ORCL",
    "Square" : "SQ",
    "NVIDIA" : "NVDA",
    "Ebay" : "EBAY",
    "Starbucks" : "SBUX",
    "Visa" : "V"
}

def BFS(s):
    # Mark all the vertices as not visited

    global visitHandles
    global conn

    heap = []
    heapq.heappush(heap, (1, s))


    while heap:
        item = heapq.heappop(heap)

        if item[1] not in visitHandles:
            visitHandles.add(item[1])

            tweets_list = tweets_scrapper.start(item[1])
            for tweet in tweets_list:
                ticker = get_ticker(tweet)
                if ticker:
                    cur = conn.cursor()
                    cur.execute('''INSERT INTO public.tweets(ticker, tweet, score, tweeter_handle) VALUES ('{}', '{}', {}, '{}');'''
                                .format(ticker, tweet.replace("'", "").replace('"', ""), item[0], item[1]))
                    conn.commit()

            following = api.friends_ids(item[1])[0:50]
            for fr in following:

                url = "https://twitter.com/intent/user?user_id=" + str(fr)

                time.sleep(10)
                content = urlopen(url)

                soup = BeautifulSoup(content, 'html.parser')
                handle = soup.find("span", class_="nickname").string
                handle = handle[1:]
                try:
                    followers = soup.find("a", href=re.compile("/followers")).string
                    followers = followers.replace(",", "")
                    verified = soup.find("li", class_="verified").string
                except AttributeError:
                    continue

                if (verified.strip() == "Verified account"):
                    heapq.heappush(heap, (int(followers) * 2 ,handle))
                else:
                    heapq.heappush(heap, (int(followers), handle))

    conn.close()

def get_ticker(tweet):
    for company in companies.items():
        if company[0].lower() in tweet.lower():
            return company[1]

    return None

if __name__ == '__main__':
    BFS("washingtonpost")