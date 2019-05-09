# coding: utf-8

import requests
import ujson
import time
from shapely.geometry import shape, point
import threading

from backend.settings import BASE_DIR


headers = {
    'X-API-KEY': '227415ba68c811e9b1a48c8590c7151e',
    'Content-Type': 'application/json'
}

melb_json = ujson.load(open(BASE_DIR + '/backend/common/melb_geo.json'))
melb_map = dict()
for zone in melb_json['features']:
    melb_map.update({zone['properties']['name']: shape(zone['geometry'])})


def process_and_update(**tweets):
    for tweet in tweets:
        geo = tweets[tweet].get('geo')
        if not geo:
            tweets[tweet]['zone'] = 'NoGeo'
        else:
            geo.sort(reverse=True)
            for zone in melb_map:
                if melb_map[zone].contains(point.Point(geo)):
                    tweets[tweet]['zone'] = zone
                    break
    try:
        resp = requests.post('http://172.26.38.1:8080/api/tweet/trained/zone/', headers=headers, json=tweets)
    except Exception:
        return


def process_zone(amount=100000, batch=10000):

    print('{} Melbourne Map Loaded {}'.format('=' * 15, '=' * 15))
    print('Amount: {}\nBatch Size: {}\n{} Start {}'.format(amount, batch,'=' * 15, '=' * 15))
    count = 1

    while amount > 0:
        try:
            resp = requests.get('http://172.26.38.1:8080/api/tweet/untrained/zone/{}/'.format(batch), headers=headers)
        except Exception as e:
            time.sleep(30)
            continue

        if resp.status_code != 200:
            time.sleep(30)
            continue

        print('Start Parallel Process: {}'.format(count))

        tweets = tuple(ujson.loads(resp.content)['data'].items())
        size = int(len(tweets) / 8)
        this_thread = []
        for i in range(8):
            this_thread.append(threading.Thread(target=process_and_update, kwargs=dict(tweets[size * i: size * (i + 1) - 1])))
            this_thread[i].setDaemon(True)
            this_thread[i].start()

        for thread in this_thread:
            thread.join()

        amount -= batch
        count += 1
        time.sleep(1)
        print('Remain: {}'.format(amount))


if __name__ == '__main__':
    process_zone(amount=100000, batch=10000)