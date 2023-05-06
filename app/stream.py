# from multiprocessing.connection import Listener
import tweepy
import configparser

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Read the values
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
bearer_token = config['twitter']['bearer_token']

# Create a StramListener
class MaxListener(tweepy.StreamingClient):

    def on_data(self, raw_data):
        self.process_data(raw_data)

        return True
    
    def process_data(self, raw_data):
        print(raw_data)
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

# Create a Stream
class MaxStream():
    def __init__(self, listener):
        self.stream = listener
    
    def start(self, keyword_list):
        self.stream.add_rules(tweepy.StreamRule(keyword_list))
        self.stream.filter()

# Start the Stream
if __name__ == "__main__":
    listener = MaxListener(bearer_token)

    # Authenticate
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = MaxStream(listener)
    stream.start(['python'])