import tweepy
from tweepy import OAuthHandler

consumer_key = 'WCqb4vOIcppLOHxJD4Z4q2xwQ'
consumer_secret = 'kWWChyjsJjeyKZQRUSDs2qnojuBhfWBXxjz11TyfqEdMmcgjEj'
access_token = '977352389421187078-E8DkXkeTkm5GYMUQkOy3mCK9BrCLOan'
access_secret = 'ZAUXyIWPlle3q5CVXl66Lfdoc5BhmN22jHQXTEYFT3R2C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


if __name__ == '__main__':
    for status in tweepy.Cursor(api.home_timeline).items(10):
        # Process a single status
        print(status.text)