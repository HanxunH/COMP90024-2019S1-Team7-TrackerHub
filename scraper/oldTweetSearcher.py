import GetOldTweets3 as got
from tweetProcess import processTweet
import mpi4py
from mpi4py import MPI


START_MSG = "1"
END_MSG = "0"

comm = MPI.COMM_WORLD
comm_size = comm.Get_size()
comm_rank = comm.Get_rank()



if comm_rank == 0 :
# use GotOldTweets to scrape past tweets without limit of time
# The scraper gets the tweets from locations within 50 miles from Melbourne Central
	tweetCriteria = got.manager.TweetCriteria().setNear('-37.80811,144.96071').setWithin('50mi')\
                                           .setSince("2018-06-01")\
                                           .setUntil("2018-12-31")\
                                           .setMaxTweets(50000)
# 
# .setUsername("GOLDFINGERS_AUS")\

# tweetlist is a list of Tweet objects defined by the library GotOldTweets
# The Tweet object here has a different format from the data scraped using Twitter Streaming API
	tweetlist = got.manager.TweetManager.getTweets(tweetCriteria)

# create a dictionary which stores the json data of each tweet


	count = 0

# For each tweet we need to exclude the retweets, also, we need to visit the url of tweet and scrape the links of images on this tweet
	for tweet in tweetlist:
		if not tweet.text.startswith('RT'):
			count+=1
			if(comm_size>1):

				if(count% comm_size != 0):

					lst = []
					lst.append(START_MSG)
					lst.append(tweet)
					comm.send(lst, dest = (count % comm_size), tag=1)

				else:
					processTweet(tweet)

			else:

				processTweet(tweet)


	if(comm_size>1):
		lst_done = [END_MSG]
		for i in range(1, comm_size):
			comm.send(lst_done, dest = i, tag=1)



if comm_rank > 0:


	while True:

		msg = comm.recv(source=0, tag = 1)

		if msg[0] == END_MSG:
			break
		
		else:
			processTweet(msg[1])













