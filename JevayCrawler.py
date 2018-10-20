import tweepy
from tweepy import OAuthHandler
import networkx as nx

consumer_key = 'WCqb4vOIcppLOHxJD4Z4q2xwQ'
consumer_secret = 'kWWChyjsJjeyKZQRUSDs2qnojuBhfWBXxjz11TyfqEdMmcgjEj'
access_token = '977352389421187078-E8DkXkeTkm5GYMUQkOy3mCK9BrCLOan'
access_secret = 'ZAUXyIWPlle3q5CVXl66Lfdoc5BhmN22jHQXTEYFT3R2C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def _getUser(userId):

    return api.get_user(userId)

def _byProtected(userId):
    user = _getUser(userId)
    return user.protected

def getFriendIds(userId, limit=100):
    if _byProtected(userId):
        return []
    friendIds = []
    try:
        friends = tweepy.Cursor(api.friends_ids, user_id=userId, cursor=-1).items()
        for cnt, friend in enumerate(friends):
            if not cnt < limit:
                break
            if friend.followers_count >= 100000:
                friendIds.append(friend)
            # print('{}, {}'.format(api.get_user(friend).screen_name, api.get_user(friend).followers_count))
        return friendIds
    except tweepy.error.TweepError as et:
        print(et)
        return []

if __name__ == '__main__':

    allFriends = []
    startFriends = getFriendIds('Developer_Joel')
    graph = nx.Graph()
    for user in startFriends:
        graph.add_edge("Developer_Joel", api.get_user(user).screen_name)

    for x in range(6):
        for user in startFriends:
            for nodeFriend in getFriendIds(user):
                graph.add_edge(api.get_user(user).screen_name, api.get_user(nodeFriend).screen_name)

    print("")
    print("The personal profile was analyzed succesfully.")
    print("")
    print("Saving the file as " + "Developer_Joel" + "-personal-network.gexf...")
    nx.write_gexf(graph, "Developer_Joel" + "-personal-network.gexf")


