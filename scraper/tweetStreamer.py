
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json as js

# My keys and tokens
consumer_key = 'U1lUxhPRqkgJnjcYxzR9l882D'
consumer_secret = 'eWyY3NaI02ZmNXT3V4ITbPGGWvrGzUyb6Lr71ecfraw8VaYQ3i'
access_token = '1118399076653944833-cpAmEuFX694kK4i7JSQy9DnRzsfZG9'
access_token_secret = 'Wh3MzRqIwqXcymvRcticPRkewb06s8DuuRiHvEXEQDdjm'

access = {"consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_secret": access_token_secret}

file = open("example.txt", "w")
# Get the authentication
def getAuth(access):

    auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
    auth.set_access_token(access['access_token'], access['access_secret'])
    return auth


#This is a basic listener that just prints received tweets to stdout.
class TweetListener(StreamListener):

	def on_data(self, data):
		tweetJson = js.loads(data, encoding= 'utf-8')
    	# need to filter out the retweets
		if not tweetJson["text"].startswith('RT'):
			file.write(data)
		return True

	def on_status(self, status):
		print(status.text)

	def on_error(self, status):
		print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = TweetListener()
    auth = getAuth(access)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data around Victoria state
    stream.filter(locations=[141, -38, 150, -35]) 
