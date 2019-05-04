import requests
import time

DOMAIN = '172.26.38.1:8080/'
TWEET_PIC_API = 'api/tweet/pic/'
TWEET_API = 'api/tweet/'
HEADERS = {
    'x-api-key': '227415ba68c811e9b1a48c8590c7151e'
}


def upload_pic(pic):
    url = 'http://{}{}'.format(DOMAIN, TWEET_PIC_API)
    files = {'file': pic}
    resp = requests.post(url=url, files=files, headers=HEADERS)
    return resp


def download_pic(pic_id):
    url = 'http://{}{}{}/'.format(DOMAIN, TWEET_PIC_API, pic_id)
    resp = requests.get(url=url, headers=HEADERS)
    return resp


def upload_tweet(tweet):
    url = 'http://{}{}'.format(DOMAIN, TWEET_API)
    headers = {
        'x-api-key': '227415ba68c811e9b1a48c8590c7151e',
        'Content-Type': 'application/json'
    }
    resp = requests.post(url=url, data=tweet, headers=headers)
    return resp


def test():
    resp = requests.get('https://abs.twimg.com/emoji/v2/72x72/1f40d.png')
    pic = resp.content
    resp = upload_pic(pic)
    print(resp.status_code, resp.content)


if __name__ == '__main__':
    while True:
        test()
        time.sleep(15)