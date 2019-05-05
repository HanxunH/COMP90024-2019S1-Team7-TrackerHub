from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
from untitled import postRequest, reformat_Image, getBinaryImage
from api_requirements import DOMAIN, API_KEY, API_PORT
from PIL import Image
from io import BytesIO
from datetime import datetime

url = "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary"
BATCHSIZE = 1000
params={'include_docs':'true','reduce':'false','start_key':"[\"melbourne\",2018,1,1]",'end_key':"[\"melbourne\",2018,12,31]", "limit": str(BATCHSIZE)}
TOTALSIZE = 300000


def uploadImg(link):

	try: 
		image = requests.get(link)
		img = Image.open(BytesIO(image.content))
		resize_img = reformat_Image(img)
		pair = {"file": getBinaryImage(resize_img, img)}
		response = postRequest(DOMAIN, API_KEY, API_PORT["upload_pic"]["Port"], API_PORT["upload_pic"]["Header"], pair, "image")
		returnMsg = json.loads(response.text)
		return returnMsg["data"]["pic_id"]



	except Exception as e:

		print(e)
		print("Cannot upload img or Cannot link to img")
		return "none"





num = 0

while num<TOTALSIZE:

	num = num + BATCHSIZE
	message=requests.get(url,params,auth=('readonly', 'ween7ighai9gahR6'))
	# Message to dict
	dataset = message.json() 
	# retrive all tweets
	tweetlst = dataset["rows"]

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
					dataDict["hashtags"].append(hashtag["text"])



			if tweet["doc"]["coordinates"]!= None and tweet["doc"]["coordinates"]["coordinates"] != None:
				dataDict["geo"] = tweet["doc"]["coordinates"]["coordinates"]

			elif tweet["doc"]["geo"]!= None and tweet["doc"]["geo"]["coordinates"] != None:
				dataDict["geo"] = tweet["doc"]["geo"]["coordinates"]

			else:
				dataDict["geo"] = []
		


			dataDict["img_id"] = []

			if "media" in tweet["doc"]["entities"] and tweet["doc"]["entities"]["media"] != None:

				for item in tweet["doc"]["entities"]["media"]:
	
					if item["media_url_https"] != None:
						return_id = uploadImg(item["media_url_https"])

						if return_id != "none":
							dataDict["img_id"].append(return_id)




			tweetJson = json.dumps(dataDict) 
			responseJson = postRequest(DOMAIN, API_KEY, API_PORT["upload_tweet"]["Port"], API_PORT["upload_tweet"]["Header"], tweetJson, "tweet")


		except Exception as e:

			print(e)
			print("Cannot upload a well-formatted tweet to couchDB")






