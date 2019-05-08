import GetOldTweets3 as got
from tweetProcess import processTweet
import argparse

parser = argparse.ArgumentParser(description='COMP90024 Project Twitter Get By User')
parser.add_argument('--username', type=str, default="IsabelleDeltore")
parser.add_argument('--startdate', type=str, default="2018-01-01")
parser.add_argument('--enddate', type=str, default="2018-12-31")
parser.add_argument('--max', type=int, default=10)
parser.add_argument('--filename', type=str, default="get_user_tweet.txt")
args = parser.parse_args()

file = open(args.filename, "w")

# use GotOldTweets to scrape past tweets without limit of time
# The scraper gets the tweets from locations within 50 miles from Melbourne Central
tweetCriteria = got.manager.TweetCriteria().setUsername(args.username)\
                                           .setSince(args.startdate)\
                                           .setUntil(args.enddate)\
                                           .setMaxTweets(args.max)


# tweetlist is a list of Tweet objects defined by the library GotOldTweets
# The Tweet object here has a different format from the data scraped using Twitter Streaming API
tweetlist = got.manager.TweetManager.getTweets(tweetCriteria)


# For each tweet we need to exclude the retweets, also, we need to visit the url of tweet and scrape the links of images on this tweet
for tweet in tweetlist:
	if not tweet.text.startswith('RT'):

		processTweet(tweet, file)


file.close()









