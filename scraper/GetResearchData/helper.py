import GetOldTweets3 as got
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from api_requirements import DOMAIN, API_KEY, API_PORT
from requests.auth import HTTPBasicAuth
from PIL import Image
from io import BytesIO



TARGET_IMG_SIZE = 256

def postRequest(domain, api_key, port, header, info, string):

	url = domain + port
	auth = HTTPBasicAuth('apikey', api_key)
	req = {}

	try:
		if string == "tweet":
			req = requests.post(url, headers=header , auth=auth, data=info)
			print("tweet being uploaded... {}".format(req.status_code))

		elif string =="image":
			req = requests.post(url, headers=header , auth=auth, files=info)
			print("image being uploaded... {}".format(req.status_code))

		

	except Exception as e:
		print(e)
		print("Some bad things happen" )

	return req


def getBinaryImage(image, original):

	# Create a buffer to hold the bytes
	buf = BytesIO()

	# Save the image as jpeg to the buffer
	image.save(buf, original.format)

	# Rewind the buffer's file pointer
	buf.seek(0)

	# Read the bytes from the buffer
	image_bytes = buf.read()

	# Close the buffer
	buf.close()

	return image_bytes


def reformat_Image(img):

	img_size = img.size
	width = img_size[0]
	height = img_size[1]

	if(width != height):
		bigside = width if width > height else height
		if img.format == "png":
			background = Image.new('RGBA', (bigside,bigside), (0,0,0))
		else:
			background = Image.new('RGB', (bigside,bigside), (0,0,0))
		offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2), 0)))
		background.paste(img, offset)
		new_img = background

	else:
		new_img = img

	result = new_img.resize((TARGET_IMG_SIZE , TARGET_IMG_SIZE))
	return result


def processTweet(tweet):

	image_urls = []
	image_ids = []
	html = urlopen(tweet.permalink)
	bs = BeautifulSoup(html, 'html.parser')
	images_jpg = bs.find_all('img', {'src':re.compile('.jpg')})
	images_png = bs.find_all('img', {'src':re.compile('.png')})
	images_jpeg = bs.find_all('img', {'src':re.compile('.jpeg')})


	# we only need to store the urls of media images, excluding emoji, profile_image, sticky..
	for jpg_file in images_jpg:
		link = str(jpg_file['src'])
		if "media" in link:
			image_urls.append(link)
	for png_file in images_png:
		link = str(png_file['src'])
		if "media" in link:
			image_urls.append(link)
		
	for jpeg_file in images_jpeg:
		link = str(jpeg_file['src'])
		if "media" in link:
			image_urls.append(link)
		
		
	if image_urls != []:
		for link in image_urls:
			try:
				image = requests.get(link)
				img = Image.open(BytesIO(image.content))
				resize_img = reformat_Image(img)

				pair = {"file": getBinaryImage(resize_img, img)}
				
				response = postRequest(DOMAIN, API_KEY, API_PORT["upload_pic"]["Port"], API_PORT["upload_pic"]["Header"], pair, "image")

				response = response.content.decode("utf-8")
				returnMsg = json.loads(response)
				image_ids.append(returnMsg["data"]["pic_id"])


			except Exception as e:

				print(e)
				print("Connot connect to image properly")


	# store all information of Tweet object as well as list of image links as Json data, which is convenient to be stored in CouchDB and retrieved for later use.
	dataDict = {}
	dataDict["id"] = tweet.id

	dataDict["user"] = tweet.username
	dataDict["text"] = tweet.text
	dataDict["date"] = tweet.date.strftime('%Y-%m-%d %H:%M:%S%z')
    

	dataDict["hashtags"] = tweet.hashtags.split()

	dataDict["geo"] = [tweet.geo]

	dataDict["img_id"] = image_ids

	tweetJson = json.dumps(dataDict) 


	responseJson = postRequest(DOMAIN, API_KEY, API_PORT["upload_tweet"]["Port"], API_PORT["upload_tweet"]["Header"], tweetJson, "tweet")
	# print(responseJson.content)










	