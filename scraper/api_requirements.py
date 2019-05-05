
import requests
DOMAIN = "http://172.26.38.1:8080/"
API_KEY = "227415ba68c811e9b1a48c8590c7151e"

API_PORT = {"upload_tweet" : {"Port" : "api/tweet/", "Header": {"Content-Type" : "application/json", "X-API-KEY": API_KEY}},
            "upload_pic" : {"Port" : "api/tweet/pic/", "Header": {"X-API-KEY": API_KEY}}
            }

