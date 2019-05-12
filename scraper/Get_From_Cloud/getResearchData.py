from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
from helper import postRequest, reformat_Image, getBinaryImage
from api_requirements import DOMAIN, API_KEY, API_PORT
from PIL import Image
from io import BytesIO
from datetime import datetime
import argparse
import time

parser = argparse.ArgumentParser(description='COMP90024 Project Scrape Research Data')
parser.add_argument('--batch', type=int, default=100)
parser.add_argument('--total', type=int, default=500)
parser.add_argument('--startDate', type=str, default='[\"sydney\",2015,1,1]')
parser.add_argument('--endDate', type=str, default='[\"sydney\",2015,12,31]')
parser.add_argument('--url', type=str, default='http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary')
parser.add_argument('--filename', type=str, default='log2016.txt')
args = parser.parse_args()

url = args.url
BATCHSIZE = args.batch
params={'include_docs':'true','reduce':'false','start_key':args.startDate,'end_key':args.endDate,"skip": "0", "limit": str(BATCHSIZE)}
TOTALSIZE = args.total

def uploadImg(link, file):

	try: 
		image = requests.get(link)
		img = Image.open(BytesIO(image.content))
		resize_img = reformat_Image(img)
		pair = {"file": getBinaryImage(resize_img, img)}
		response = postRequest(DOMAIN, API_KEY, API_PORT["upload_pic"]["Port"], API_PORT["upload_pic"]["Header"], pair, "image", file)
		returnMsg = json.loads(response.text)
		return returnMsg["data"]["pic_id"]



	except Exception as e:

		print(e)
		print("Cannot upload img or Cannot link to img")
		file.write(str(e) + "\n")
		file.write("Cannot upload img or Cannot link to img\n")
		return "none"





num = 0
file = open(args.filename,"w")
while num<TOTALSIZE:

	message=requests.get(url,params,auth=('readonly', 'ween7ighai9gahR6'))


	num = num + BATCHSIZE
	
	temp = num
	params['skip'] = str(temp)
	# Message to dict
	dataset = message.json()

	# retrive all tweets
	tweetlst = dataset["rows"]
	print(str(num) + "Tweets scraped")
	file.write(str(num) + "Tweets scraped\n")
	for tweet in tweetlst:


		try:

			dataDict = {}
			dataDict["id"] = tweet["id"]
			dataDict["user"] = tweet["doc"]["user"]["screen_name"]
			dataDict["text"] = tweet["doc"]["text"]

			if tweet["doc"]["created_at"] != None:
				stringTime = tweet["doc"]["created_at"]
				dataDict["date"] = datetime.strptime(stringTime,'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')


			else:
				dataDict["date"] = ""
    		
			dataDict["hashtags"] = []

			if tweet["doc"]["entities"]["hashtags"] != None:

				listHashtags = tweet["doc"]["entities"]["hashtags"]
				for hashtag in listHashtags:
					if "text" in hashtag.keys(): 		
						dataDict["hashtags"].append(hashtag["text"])



			if tweet["doc"]["coordinates"]!= None and tweet["doc"]["coordinates"]["coordinates"] != None:
				dataDict["geo"] = tweet["doc"]["coordinates"]["coordinates"]

			elif tweet["doc"]["geo"]!= None and tweet["doc"]["geo"]["coordinates"] != None:
			
				temp = tweet["doc"]["geo"]["coordinates"]				
				if len(temp) == 2:
					dataDict["geo"] = [temp[1], temp[0]]


			else:
				dataDict["geo"] = []
		


			dataDict["img_id"] = []

			if "media" in tweet["doc"]["entities"] and tweet["doc"]["entities"]["media"] != None:

				for item in tweet["doc"]["entities"]["media"]:
	
					if item["media_url_https"] != None:
						return_id = uploadImg(item["media_url_https"], file)

						if return_id != "none":
							dataDict["img_id"].append(return_id)




			tweetJson = json.dumps(dataDict) 
			responseJson = postRequest(DOMAIN, API_KEY, API_PORT["upload_tweet"]["Port"], API_PORT["upload_tweet"]["Header"], tweetJson, "tweet" , file)

		except Exception as e:

			print(e)
			print("Cannot upload a well-formatted tweet to couchDB")
			file.write(str(e) + "\n")
			file.write("Cannot upload a well-formatted tweet to couchDB\n")


file.close()
