
import tweepy
from tweepy.streaming import StreamListener
from api_requirements import DOMAIN, API_KEY, API_PORT
from tweepy import OAuthHandler
from tweepy import Stream
import json as js
import argparse
from datetime import datetime
from tweetProcess import uploadImg, postRequest

# My keys and tokens
consumer_key = 'U1lUxhPRqkgJnjcYxzR9l882D'
consumer_secret = 'eWyY3NaI02ZmNXT3V4ITbPGGWvrGzUyb6Lr71ecfraw8VaYQ3i'
access_token = '1118399076653944833-cpAmEuFX694kK4i7JSQy9DnRzsfZG9'
access_token_secret = 'Wh3MzRqIwqXcymvRcticPRkewb06s8DuuRiHvEXEQDdjm'

access = {"consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_secret": access_token_secret}


# Get the authentication
def getAuth(access):

    auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
    auth.set_access_token(access['access_token'], access['access_secret'])
    return auth


def dealStream(tweetJson, file):


    try:
        dataDict = {}
        dataDict["id"] = tweetJson["id_str"]
        dataDict["user"] = tweetJson["user"]["screen_name"]
        dataDict["text"] = tweetJson["text"]

        if tweetJson["created_at"] != None:
            stringTime = tweetJson["created_at"]
            dataDict["date"] = datetime.strptime(stringTime,'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
        else:
            dataDict["date"] = ""
            
        dataDict["hashtags"] = []

        if tweetJson["entities"]["hashtags"] != None:

            listHashtags = tweetJson["entities"]["hashtags"]
            for hashtag in listHashtags:        
                dataDict["hashtags"].append(hashtag["text"])

        elif tweetJson["extended_tweet"] != None and tweetJson["extended_tweet"]["entities"] != None and tweetJson["extended_tweet"]["entities"]["hashtags"] != None:
            
            listHashtags = tweetJson["extended_tweet"]["entities"]["hashtags"]
            for hashtag in listHashtags:        
                dataDict["hashtags"].append(hashtag["text"])            



        if tweetJson["coordinates"]!= None and tweetJson["coordinates"]["coordinates"] != None:
            dataDict["geo"] = tweetJson["coordinates"]["coordinates"]

        elif tweetJson["geo"]!= None and tweetJson["geo"]["coordinates"] != None:
            temp = tweetJson["geo"]["coordinates"]
            if len(temp) == 2:
                dataDict["geo"] = [temp[1], temp[0]]

        else:
            dataDict["geo"] = []
        


        dataDict["img_id"] = []

        if "extended_tweet" in tweetJson.keys() and tweetJson["extended_tweet"] != None and "extended_entities" in tweetJson["extended_tweet"] and \
        tweetJson["extended_tweet"]["extended_entities"] != None and "media" in tweetJson["extended_tweet"]["extended_entities"]\
        and tweetJson["extended_tweet"]["extended_entities"]["media"] != None:

            for item in tweetJson["extended_tweet"]["extended_entities"]["media"]:
                if item["media_url"] != None:
                    return_id = uploadImg(item["media_url"], file)
                    if return_id != "none":
                        dataDict["img_id"].append(return_id)  

                elif item["media_url_https"] != None:   
                    return_id = uploadImg(item["media_url_https"], file)
                    if return_id != "none":
                        dataDict["img_id"].append(return_id)                 

        newJson = js.dumps(dataDict) 
        responseJson = postRequest(DOMAIN, API_KEY, API_PORT["upload_tweet"]["Port"], API_PORT["upload_tweet"]["Header"], newJson, "tweet", file)


    except Exception as e:

        print(e)
        print("Cannot upload a well-formatted tweet to couchDB")
        file.write(str(e) + "\n")
        file.write("Cannot upload a well-formatted tweet to couchDB\n")



parser = argparse.ArgumentParser(description='COMP90024 Project Twitter Streamer')
# Use like:
# python arg.py -l 1234 2345 3456 4567
parser.add_argument('-l','--list', nargs='+', default=[141, -38, 150, -35])
parser.add_argument('--filename', type=str, default="streamlog.txt")
args = parser.parse_args()



file = open(args.filename, "w")

#This is a basic listener that just prints received tweets to stdout.
class TweetListener(StreamListener):

    def on_data(self, data):

        tweetJson = js.loads(data, encoding= 'utf-8')
        print(tweetJson)
    	# need to filter out the retweets
        if not tweetJson["text"].startswith('RT') and tweetJson["retweeted"] == False:
            file.write(data)
            dealStream(tweetJson, file)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    
    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = TweetListener()
    auth = getAuth(access)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data around Victoria state
    stream.filter(locations=args.list) 

    file.close()





