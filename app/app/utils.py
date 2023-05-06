import configparser
import tweepy
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import sqlite3    


class StreamListener(tweepy.StreamingClient):
    def __init__(self, bearer_token, table):
        self.table = table  
        
    def on_status(self, status):
        if status.retweeted:
            return

        author_name = status.user.name
        name = status.user.screen_name
        created = status.created_at
        text = status.text
        description = status.user.description
        prof_image = status.user.profile_image_url
        loc = status.user.location
        coords = status.coordinates
        geo = status.geo
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)

        # table = db[TABLE_NAME]
        try:
            self.table.insert(dict(
                author = author_name,
                user_name=name,
                created=created,
                text=text,
                user_description=description,
                profile_image = prof_image,
                user_location=loc,
                coordinates=coords,
                geo=geo,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sent.polarity,
                subjectivity=sent.subjectivity,
            ))

        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


class TwitterPosts:
    def __init__(self):
        # Read the config file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Read the values
        self.bearer_token = self.config['twitter']['bearer_token']
        self.api_key = self.config['twitter']['api_key']
        self.api_key_secret = self.config['twitter']['api_key_secret']
        self.access_token = self.config['twitter']['access_token']
        self.access_token_secret = self.config['twitter']['access_token_secret']
        # self.TRACK_TERMS = ["trump", "clinton", "sanders", "hillary clinton", "bernie", "donald trump"]
        CONNECTION_STRING = "sqlite:///tweets.db"
        # self.CSV_NAME = "tweets.csv"
        TABLE_NAME = "tweet"

        db = dataset.connect(CONNECTION_STRING)
        self.table = db[TABLE_NAME]

    def getposts(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        public_tweets = api.home_timeline(tweet_mode='extended')
        for status in public_tweets:
            author_name = status.user.name
            name = status.user.screen_name
            created = status.created_at
            text = status.full_text
            description = status.user.description
            prof_image = status.user.profile_image_url
            loc = status.user.location
            coords = status.coordinates
            geo = status.geo
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            retweets = status.retweet_count
            bg_color = status.user.profile_background_color
            blob = TextBlob(text)
            sent = blob.sentiment
            self.table.insert(dict(
                        author = author_name,
                        user_name=name,
                        created=created,
                        text=text,
                        user_description=description,
                        profile_image = prof_image,
                        user_location=loc,
                        coordinates=coords,
                        geo=geo,
                        user_created=user_created,
                        user_followers=followers,
                        id_str=id_str,
                        retweet_count=retweets,
                        user_bg_color=bg_color,
                        polarity=sent.polarity,
                        subjectivity=sent.subjectivity,
                    ))

        # stream_listener = StreamListener()
        stream = StreamListener(self.bearer_token, self.table)
        # stream.add_rules(tweepy.StreamRule("donald trump"))
        # stream.add_rules(tweepy.StreamRule("hillary clinton"))
        # stream.filter()
        # # stream.filter(track=TRACK_TERMS)
        conn = sqlite3.connect('tweets.db')    
        cursor = conn.cursor()    
        data = cursor.execute('''SELECT * From tweet order by created asc;''')
        return data
if __name__ == '__main__':
    twitter_posts = TwitterPosts()
    posts = twitter_posts.getposts()