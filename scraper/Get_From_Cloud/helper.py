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

def postRequest(domain, api_key, port, header, info, string, file):

	url = domain + port
	auth = HTTPBasicAuth('apikey', api_key)
	req = {}

	try:
		if string == "tweet":
			req = requests.post(url, headers=header , auth=auth, data=info)
			print(req.text)
			print("tweet being uploaded... {}".format(req.status_code))
			file.write("tweet being uploaded... {}\n".format(req.status_code))

		elif string =="image":
			req = requests.post(url, headers=header , auth=auth, files=info)
			print("image being uploaded... {}".format(req.status_code))
			file.write("image being uploaded... {}\n".format(req.status_code))

		

	except Exception as e:
		print(e)
		print("Some bad things happen" )
		file.write(str(e) + "\n")
		file.write("Some bad things happen\n")
		

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











	