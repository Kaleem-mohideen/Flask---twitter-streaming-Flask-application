import configparser
import tweepy
import pandas as pd

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the values
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
bearer_token = config['twitter']['bearer_token']
# Authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Fetch public tweets from home timeline
public_tweets = api.home_timeline(tweet_mode='extended')
print(public_tweets[0])
print(public_tweets[0].user.name)
print(public_tweets[0].user.description)
print(public_tweets[0].user.screen_name)
print(public_tweets[0].full_text)

# for tweet in public_tweets:
#     print(tweet.text)
data = []

for tweet in public_tweets:
    data.append([tweet.id, tweet.created_at, tweet.user.screen_name, tweet.full_text, tweet.user.screen_name, tweet.user.description, tweet.user.name])


class Linstener(tweepy.StreamingClient):

    tweets = []
    limit = 1

    def on_status(self, status):
        self.tweets.append(status)
        # print(status.user.screen_name + ": " + status.text)

        if len(self.tweets) == self.limit:
            self.disconnect()
    def on_error(self, status):
        print(status)


stream_tweet = Linstener(bearer_token)#api_key, api_key_secret, access_token, access_token_secret)

# stream by keywords
# keywords = ['2022', '#python']

# stream_tweet.filter(track=keywords)

# stream by users
users = ['mohideen_kaleem']
user_ids = []

# for user in users:
#     user_ids.append(api.get_user(screen_name=user).id)
# stream_tweet.add_rules(tweepy.StreamRule("from:mohideen_kaleem"))
# stream_tweet.filter()

columns = ['TweetId', 'Time', 'User', 'Tweet', 'User_name', 'Description', 'Author']

for tweet in stream_tweet.tweets:
    if not tweet.truncated:
        data.append([tweet.id, tweet.created_at, tweet.user.screen_name, tweet.text, tweet.user.screen_name, tweet.user.description, tweet.user.name])
    else:
        data.append([tweet.id, tweet.created_at, tweet.user.screen_name, tweet.extended_tweet['full_text'], tweet.user.screen_name, tweet.user.description, tweet.user.name])

df = pd.DataFrame(data, columns=columns)
print(df)
df.to_csv('tweets.csv')