from api_requirements import DOMAIN, API_KEY, API_PORT
import requests
from pyspark import SparkContext, SparkConf
import time, re
from text_analysis import lust_analysis,profanity_analysis, sentiment_analysis
import argparse
from requests.auth import HTTPBasicAuth
import json
import time

parser = argparse.ArgumentParser(description='COMP90024 Project Text Analysis')
parser.add_argument('--batch', type=int, default=500)
parser.add_argument('--total', type=int, default=3000)
parser.add_argument('--filename', type=str, default="Analysis_Log.txt")
parser.add_argument('--setmaster', type=str, default="local[4]")
args = parser.parse_args()

params = {"skip": "0"}
BATCHSIZE = args.batch
TOTALSIZE = args.total

file = open(args.filename, "w+")


URL = DOMAIN + API_PORT["update_tweet"]["Port"]
AUTH = HTTPBasicAuth('apikey',  API_KEY)
HEADER = API_PORT["update_tweet"]["Header"]


def getRequest(domain, api_key, port, header, params, num, file):

	url = domain + port + str(num)
	auth = HTTPBasicAuth('apikey', api_key)
	req = {}
	tweetDict = {}
	try:

		req = requests.get(url, params, headers=header , auth=auth)
		returnMsg = json.loads(req.text)
		tweetDict = returnMsg['data']



	except Exception as e:
		print(e)
		print("Some bad things happen" )
		file.write(str(e) + "\n")
		file.write("Some bad things happen\n")

	return tweetDict


def updateTweet(pair):

	succeed = 1

	# for pair in iterator:
	text = pair[0]
	index = pair[1]
	result_lust = lust_analysis(text)
	result_violence = 0
	if profanity_analysis(text):
		result_violence = 1

	result_sentiment = sentiment_analysis(text)

	form = {}
	form[index] = {}
	form[index]['tags'] ={}
	form[index]['tags']['text'] ={}
	form[index]['tags']['text']["lust"] = result_lust
	form[index]['tags']['text']["wrath"] = result_violence
	form[index]['tags']['text']["sentiment"] = result_sentiment
	formjson = json.dumps(form)


	try:

		updateResponse = requests.post(URL, headers = HEADER, auth = AUTH, data = formjson)
		print(json.loads(updateResponse.text))

	except Exception as e:

		print(e)
		print("Something bad happened on analysis")
		succeed = 0

	if succeed:

		# return [1 for pair in iterator]
		return ("true", index)

	else:

		# return [0 for pair in iterator]
		return ("false", index)



def main():

	num = 0

	conf = SparkConf().setAppName("Text analysis").setMaster(args.setmaster)
	sc = SparkContext(conf=conf)


	while num< TOTALSIZE:

		
		num = num + BATCHSIZE

		

		response = getRequest(DOMAIN, API_KEY, API_PORT["download_tweet"]["Port"], API_PORT["download_tweet"]["Header"], params, BATCHSIZE, file)


		if type(response) == type(dict()) and len(response.keys()) != 0:


			file.write("{} tweets has been retrieved and waiting for analysis...\n".format(num))
		# list of (text, id) pair
			infoList = []

			for id_str in response.keys():
				infoList.append((response[id_str]['text'], id_str))

			results = sc.parallelize(infoList).map(lambda pair: updateTweet(pair)).collect()
			print(results)


			flag = 0
			for item in results:
				if "true" not in item: 
					file.write("Something happened, stop analysis\n")
					flag = 1
					break
			if flag == 0:
				file.write("{} tweets has been analyzed and updateed\n".format(num))

		elif type(response) == type(dict()) and len(response.keys()) == 0:

			file.write("No new data!\n")
			time.sleep(1800)

		else:
			file.write("Bad GET request, stop analysis\n")
			time.sleep(30)



	sc.stop()
	file.close()


if __name__ == "__main__":
	main()









