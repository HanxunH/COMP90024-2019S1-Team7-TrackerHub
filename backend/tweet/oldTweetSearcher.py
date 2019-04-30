import GetOldTweets3 as got
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

file = open("oldTwitters.json", "w")


# use GotOldTweets to scrape past tweets without limit of time
# The scraper gets the tweets from locations within 50 miles from Melbourne Central
tweetCriteria = got.manager.TweetCriteria().setNear('-37.80811,144.96071').setWithin('50mi')\
                                           .setSince("2015-05-01")\
                                           .setUntil("2018-09-30")\
                                           .setMaxTweets(2)


# tweetlist is a list of Tweet objects defined by the library GotOldTweets
# The Tweet object here has a different format from the data scraped using Twitter Streaming API
tweetlist = got.manager.TweetManager.getTweets(tweetCriteria)

# create a dictionary which stores the json data of each tweet
Data = {}
Data["tweets"] = []

# For each tweet we need to exclude the retweets, also, we need to visit the url of tweet and scrape the links of images on this tweet
for tweet in tweetlist:
	if not tweet.text.startswith('RT'):
		image_urls = []
		html = urlopen(tweet.permalink)
		bs = BeautifulSoup(html, 'html.parser')
		images_jpg = bs.find_all('img', {'src':re.compile('.jpg')})
		images_png = bs.find_all('img', {'src':re.compile('.png')})

		for jpg_file in images_jpg:
			image_urls.append(str(jpg_file['src']))
		for png_file in images_png:
			image_urls.append(str(png_file['src']))
		
		# store all information of Tweet object as well as list of image links as Json data, which is convenient to be stored in CouchDB and retrieved for later use.
		dataDict = {}
		dataDict["id"] = tweet.id
		dataDict["link"] = tweet.permalink
		dataDict["user"] = tweet.username
		dataDict["text"] = tweet.text
		dataDict["date"] = str(tweet.date)
		dataDict["hashtags"] = tweet.hashtags
		dataDict["geo"] = tweet.geo
		dataDict["urls"] = tweet.urls
		dataDict["image_urls"] = image_urls
		Data["tweets"].append(dataDict)


json.dump(Data, file, indent=4)

	

