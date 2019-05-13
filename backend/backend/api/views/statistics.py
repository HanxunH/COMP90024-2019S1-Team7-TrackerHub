# coding: utf-8
"""
@Author: Lihuan Zhang

This file including the views that used to return statistics results
"""

import logging
import ujson
import time

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from backend.handler.couch_handler import couch_db_banlancer
from backend.handler.influxdb_handler import influxdb_handler
from backend.handler.object_storage_handler import json_storage_handler
from backend.common.utils import make_dict, init_http_not_found, init_http_success, check_api_key, make_json_response, \
    str_to_str_datetime_utc
from backend.settings import BASE_DIR

logger = logging.getLogger('django.debug')
tweet_couch_db = couch_db_banlancer
melb_json = ujson.load(open(BASE_DIR + '/backend/common/melb_geo.json'))


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def statistics_time_router(request, *args, **kwargs):
    """
    TODO: Implement the function
    """
    if request.method == 'POST':
        return statistics_time_get(request)
    elif request.method == 'OPTIONS':
        return HttpResponse()
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'OPTIONS'])
@check_api_key
def statistics_track_router(request, *args, **kwargs):
    """
    A router used to check the request is used to track random users or certain user
    """
    user_id = None
    number = 100
    for arg in args:
        if isinstance(arg, dict):
            user_id = arg.get('user_id', None)
            number = arg.get('number', 100)

    if request.method == 'POST':
        return statistics_track_get(request, user_id=user_id, number=number)
    elif request.method == 'OPTIONS':
        return HttpResponse()
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def statistics_zone_router(request, *args, **kwargs):
    """
    A router used to control the permission
    """
    for arg in args:
        if isinstance(arg, dict):
            zone = arg.get('zone', None)

    if request.method == 'GET':
        return statistics_zone_get(request, zone)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def statistics_zone_vic_router(request, *args, **kwargs):
    """
    A router used to control the permission
    """
    for arg in args:
        if isinstance(arg, dict):
            zone = arg.get('zone', None)

    if request.method == 'GET':
        return statistics_zone_vic_get(request, zone)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def statistics_machine_router(request, *args, **kwargs):
    """
    A router used to control the permission
    """
    if request.method == 'GET':
        return statistics_machine_get(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def statistics_text_router(request, *args, **kwargs):
    """
    A router used to control the permission
    """
    if request.method == 'GET':
        return statistics_text_get(request)
    return HttpResponseNotAllowed()


def statistics_zone_get(request, zone=None):
    """
    Return the statistics results according to the zone of Melbourne
    """

    start_timer = time.time()

    today = timezone.now().strftime('%Y-%m-%d')
    json_name = 'zone-{}.json'.format(today)

    melb_json = ujson.load(open(BASE_DIR + '/backend/common/melb_geo.json'))

    try:
        # Check if there is a cached results
        if json_storage_handler.find(json_name):
            timer = (time.time() - start_timer)
            influxdb_handler.make_point(key='api/statistics/zone/', method='GET', error='success', prefix='API',
                                        timer=timer)

            # Return cached results directly
            resp = init_http_success()
            resp['data'].update(dict(url='http://172.26.38.1:8080/api/statistics/file/%s/' % json_name))
            return make_json_response(HttpResponse, resp)
    except Exception:
        pass

    current_db = tweet_couch_db.get_current_database()
    tweets = current_db.view('statistics/zone_tags', stale='ok', group=True, group_level=3)
    results = dict()
    for tweet in tweets:
        if tweet.key[0] not in results:
            results.update({tweet.key[0]: {}})
        if tweet.key[1] == 'food179':
            tweet.key[1] = 'gluttony'
        if tweet.key[1] == 'nsfw':
            tweet.key[1] = 'lust'
        if tweet.key[1] not in results[tweet.key[0]]:
            results[tweet.key[0]].update({tweet.key[1]: {}})
        if 'sentiment' not in results[tweet.key[0]]:
            results[tweet.key[0]].update(dict(sentiment={}))
        if tweet.key[2] not in results[tweet.key[0]][tweet.key[1]] and tweet.key[2] not in ['non_food', 'neutral']:
            if '.' in tweet.key[2]:
                if 'sentiment' in tweet.key[2]:
                    results[tweet.key[0]]['sentiment'].update({tweet.key[2].split('.')[1]: tweet.value})
                else:
                    results[tweet.key[0]][tweet.key[1]].update({tweet.key[2].split('.')[1]: tweet.value})
                continue
            results[tweet.key[0]][tweet.key[1]].update({tweet.key[2]: tweet.value})

    for result in results:
        total = 0
        for melb_zone in melb_json['features']:
            if melb_zone['properties']['name'] == result:
                if 'gluttony' in results[result]:
                    for item in results[result]['gluttony']:
                        total += results[result]['gluttony'][item]
                if 'lust' in results[result]:
                    for item in results[result]['lust']:
                        total += results[result]['lust'][item]
                if 'text' in results[result]:
                    for item in results[result]['text']:
                        total += results[result]['text'][item]
                melb_zone['properties'].update(dict(statistcs=results[result], total=total))

    # Upload the results to Nectar Object Storage as cache
    json_file = ujson.dumps(melb_json)
    try:
        json_storage_handler.upload(json_name, json_file)
    except Exception as e:
        json_storage_handler.reconnect()
        json_storage_handler.upload(json_name, json_file)

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/statistics/zone/', method='GET', error='success', prefix='API', timer=timer)
    resp = init_http_success()
    resp['data'].update(dict(url='http://172.26.38.1:8080/api/statistics/file/%s/' % json_name))
    return make_json_response(HttpResponse, resp)


def statistics_zone_vic_get(request, zone=None):
    """
    Return the statistics results according to the zone of Victoria State
    """

    start_timer = time.time()

    today = timezone.now().strftime('%Y-%m-%d')
    json_name = 'zone-vic-{}.json'.format(today)

    vic_json = ujson.load(open(BASE_DIR + '/backend/common/vic_geo.json'))

    try:
        # Check if there is a cached results
        if json_storage_handler.find(json_name):
            timer = (time.time() - start_timer)
            influxdb_handler.make_point(key='api/statistics/zone/vic/', method='GET', error='success', prefix='API',
                                        timer=timer)

            # Return cached results directly
            resp = init_http_success()
            resp['data'].update(dict(
                url='http://172.26.38.1:8080/api/statistics/file/%s/' % json_name))
            return make_json_response(HttpResponse, resp)
    except Exception:
        pass

    current_db = tweet_couch_db.get_current_database()
    tweets = current_db.view('statistics/vic_zone_tags', stale='ok', group=True, group_level=3)
    results = dict()
    for tweet in tweets:
        if tweet.key[0] not in results:
            results.update({tweet.key[0]: {}})
        if tweet.key[1] == 'food179':
            tweet.key[1] = 'gluttony'
        if tweet.key[1] == 'nsfw':
            tweet.key[1] = 'lust'
        if tweet.key[1] not in results[tweet.key[0]]:
            results[tweet.key[0]].update({tweet.key[1]: {}})
        if 'sentiment' not in results[tweet.key[0]]:
            results[tweet.key[0]].update(dict(sentiment={}))
        if tweet.key[2] not in results[tweet.key[0]][tweet.key[1]] and tweet.key[2] not in ['non_food', 'neutral']:
            if '.' in tweet.key[2]:
                if 'sentiment' in tweet.key[2]:
                    results[tweet.key[0]]['sentiment'].update({tweet.key[2].split('.')[1]: tweet.value})
                else:
                    results[tweet.key[0]][tweet.key[1]].update({tweet.key[2].split('.')[1]: tweet.value})
                continue
            results[tweet.key[0]][tweet.key[1]].update({tweet.key[2]: tweet.value})

    for result in results:
        total = 0
        for vic_zone in vic_json['features']:
            if vic_zone['properties']['vic_lga__3'] == result:
                if 'gluttony' in results[result]:
                    for item in results[result]['gluttony']:
                        total += results[result]['gluttony'][item]
                if 'lust' in results[result]:
                    for item in results[result]['lust']:
                        total += results[result]['lust'][item]
                if 'text' in results[result]:
                    for item in results[result]['text']:
                        total += results[result]['text'][item]
                vic_zone['properties'].update(dict(name=result))
                vic_zone['properties'].update(dict(statistcs=results[result], total=total))

    # Upload the results to Nectar Object Storage as cache
    json_file = ujson.dumps(vic_json)
    try:
        json_storage_handler.upload(json_name, json_file)
    except Exception as e:
        json_storage_handler.reconnect()
        json_storage_handler.upload(json_name, json_file)

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/statistics/zone/vic/', method='GET', error='success', prefix='API',
                                timer=timer)
    resp = init_http_success()
    resp['data'].update(
        dict(url='http://172.26.38.1:8080/api/statistics/file/%s/' % json_name))
    return make_json_response(HttpResponse, resp)


def statistics_machine_get(request):
    """
    Return the statistics results of Machine Learning
    """
    start_timer = time.time()

    today = timezone.now().strftime('%Y-%m-%d')
    json_name = 'machine\\{}.json'.format(today)

    try:
        # Check if there is a cached results
        result_file = json_storage_handler.download(json_name)
        results = ujson.load(result_file)

        timer = (time.time() - start_timer)
        influxdb_handler.make_point(key='api/statistics/machine/', method='GET', error='success', prefix='API',
                                    timer=timer)
        resp = init_http_success()
        resp['data'] = results
        return make_json_response(HttpResponse, resp)
    except Exception:
        pass

    while True:
        try:
            current_db = tweet_couch_db.get_current_database()
            results = current_db.view('statistics/machine_result', group=True, stale='ok')
            results = dict((result.key, result.value) for result in results)
            break
        except Exception as e:
            logger.debug('Query Timeout %s' % e)
            influxdb_handler.make_point(key='api/statistics/machine/', method='GET', error=500, prefix='API')
            continue

    lust = dict()
    gluttony = dict(others=0)
    for result in results:
        if result in ['neutral', 'sexy', 'porn', 'hentai', 'drawings']:
            lust.update({result: results[result]})
        elif results[result] < 10:
            gluttony['others'] += results[result]
        else:
            gluttony.update({result: results[result]})
    lust = dict(sorted(lust.items(), key=lambda item: item[1], reverse=True))
    gluttony = dict(sorted(gluttony.items(), key=lambda item: item[1], reverse=True))

    lust = dict(key=lust.keys(), value=lust.values())
    gluttony = dict(key=gluttony.keys(), value=gluttony.values())
    results = dict(lust=lust, gluttony=gluttony)

    # Upload the results to Nectar Object Storage as cache
    json_file = ujson.dumps(results)
    try:
        json_storage_handler.upload(json_name, json_file)
    except Exception as e:
        json_storage_handler.reconnect()
        json_storage_handler.upload(json_name, json_file)

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/statistics/machine/', method='GET', error='success', prefix='API', timer=timer)
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def statistics_text_get(request):
    """
    Return the statistics results for Natural Language Process
    """

    start_timer = time.time()

    today = timezone.now().strftime('%Y-%m-%d')
    json_name = 'text\\{}.json'.format(today)

    try:
        # Check if there is a cached results
        result_file = json_storage_handler.download(json_name)
        results = ujson.load(result_file)

        timer = (time.time() - start_timer)
        influxdb_handler.make_point(key='api/statistics/text/', method='GET', error='success', prefix='API',
                                    timer=timer)
        resp = init_http_success()
        resp['data'] = results
        return make_json_response(HttpResponse, resp)
    except Exception:
        pass

    while True:
        try:
            current_db = tweet_couch_db.get_current_database()
            results = current_db.view('statistics/text_result', group=True, stale='ok')
            results = dict((result.key, result.value) for result in results)
            break
        except Exception as e:
            logger.debug('Query Timeout %s' % e)
            influxdb_handler.make_point(key='api/statistics/text/', method='GET', error=500, prefix='API')
            continue

    text = dict()
    sentiment = dict()
    for result in results:
        if result in ['neutral', 'positive', 'negative']:
            sentiment.update({result: results[result]})
        else:
            text.update({result: results[result]})

    sentiment = dict(sorted(sentiment.items(), key=lambda item: item[1], reverse=True))
    text = dict(sorted(text.items(), key=lambda item: item[1], reverse=True))
    sentiment = dict(key=sentiment.keys(), value=sentiment.values())
    text = dict(key=text.keys(), value=text.values())
    results = dict(text=text, sentiment=sentiment)

    # Upload the results to Nectar Object Storage as cache
    json_file = ujson.dumps(results)
    try:
        json_storage_handler.upload(json_name, json_file)
    except Exception as e:
        json_storage_handler.reconnect()
        json_storage_handler.upload(json_name, json_file)

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/statistics/text/', method='GET', error='success', prefix='API', timer=timer)
    resp = init_http_success()
    resp['data'] = results
    return make_json_response(HttpResponse, resp)


def statistics_time_get(request):
    pass


def upload_statistics_file():
    pass


def down_statistics_file(request):
    pass


def statistics_track_get(request, user_id=None, number=100):
    """
    This function is used to track one user of random user
    """

    def process_tag(tags):
        result_tags = {}
        for tag in tags:
            if tag in ['hentai', 'porn']:
                result_tags.update({'lust': [tag]})
            elif tag in ['neutral', 'positive', 'negative']:
                result_tags.update({'sentiment': [tag]})
            elif 'text' in tag:
                result_tags.update({'text': [tag.lstrip('text.')]})
            else:
                result_tags.update({'gluttony': [tag]})
        return result_tags

    def make_this_point(_length, _timer):
        if user_id:
            influxdb_handler.make_point(key='api/statistics/track/:user_id/', method='GET', error='success',
                                        prefix='API', user=_length, timer=_timer)
        else:
            influxdb_handler.make_point(key='api/statistics/track/random/', method='GET', error='success', prefix='API',
                                        user=_length, timer=_timer)

    start_timer = time.time()

    params = ujson.loads(request.body) if request.body else {}
    start_time = params.get('start_time', None)
    end_time = params.get('end_time', None)
    target_tag = params.get('tags', [])
    skip = params.get('skip', 0)
    single = int(params.get('single', 50))

    try:
        start_time = str_to_str_datetime_utc(start_time) if start_time else None
        end_time = str_to_str_datetime_utc(end_time) if end_time else None
    except Exception as e:
        resp = init_http_not_found('Data time format error')
        return make_json_response(HttpResponseBadRequest, resp)

    number = 1 if user_id else number
    today = timezone.now().strftime('%Y-%m-%d')

    json_name = 'track\\{}\\{}\\{}\\{}.json'
    json_name = json_name.format(user_id, None if not start_time else start_time.replace(' ', '-'),
                                 None if not end_time else end_time.replace(' ', '-'), today)

    try:
        # Check if there is a cached results
        result_file = json_storage_handler.download(json_name)
        results = ujson.load(result_file)

        # Process the cached results to meet the input parameter requirement
        results = dict(tuple(results.items())[skip: skip + number])
        for user in results:
            new_tweet = []
            for tweet in results[user]:
                result_tag = {}

                if user_id and ((start_time and parse_datetime(tweet['time']) < parse_datetime(start_time)) or (
                        end_time and parse_datetime(tweet['time']) > parse_datetime(end_time))):
                    continue
                for tag in tweet['tags']:
                    if tag in target_tag or tweet['tags'][tag] in target_tag:
                        result_tag.update({tag: tweet['tags'][tag]})

                tweet['tags'] = result_tag
                if result_tag or not target_tag:
                    new_tweet.append(tweet)
            results[user] = new_tweet

            results[user] = results[user][0:single]
            results[user].sort(key=lambda x: x.get('time'))
        results = dict(sorted(results.items(), key=lambda item: len(item[1]), reverse=True))

        timer = (time.time() - start_timer)

        make_this_point(len(results), timer)
        resp = init_http_success()
        resp['data'].update(results)
        return make_json_response(HttpResponse, resp)
    except Exception as e:
        pass

    # Avoid possible query timeout
    while True:
        try:
            current_db = tweet_couch_db.get_current_database()
            if not user_id:
                tweets = current_db.view('statistics/time_geo_all_tags', startkey=start_time, endkey=end_time,
                                         stale='ok', limit=100000)
            else:
                tweets = current_db.view('statistics/user_geo', key=user_id, stale='ok', limit=single)
            tweets = [tweet.value for tweet in tweets]
            break
        except Exception as e:
            logger.debug('Query Timeout %s' % e)
            influxdb_handler.make_point(key='api/statistics/track/:user_id/', method='GET', error=500, prefix='API')
            continue

    results = {}
    geo_exists = {}
    for tweet in tweets:
        user = tweet.get('user')
        results.update({user: []}) if user not in results else None
        geo_exists.update({user: []}) if user not in geo_exists else None

        if tweet.get('geo') not in geo_exists[user] and len(results[user]) < 150:
            geo_exists[user].append(tweet.get('geo'))
            results[user].append(dict(
                time=parse_datetime(tweet.get('date')).astimezone(timezone.get_current_timezone()).strftime(
                    '%Y-%m-%d %H:%M:%S%z'),
                geo=tweet.get('geo'),
                img_id=tweet.get('img_id'),
                tags=process_tag(tweet.get('tags'))
            ))
            if user_id:
                results[user][-1].update(dict(text=tweet.get('text')))

    results = dict(sorted(results.items(), key=lambda item: len(item[1]), reverse=True))
    for user in results:
        results[user].sort(key=lambda x: x.get('time'))

    # Upload the origin query results to Nectar Object Storage as cache
    json_file = ujson.dumps(results)
    try:
        json_storage_handler.upload(json_name, json_file)
    except Exception as e:
        json_storage_handler.reconnect()
        json_storage_handler.upload(json_name, json_file)

    # Process the results according th input parameters
    results = dict(tuple(results.items())[skip: skip + number])
    for user in results:
        new_tweet = []
        for tweet in results[user]:
            result_tag = {}

            if user_id and ((start_time and parse_datetime(tweet['time']) < parse_datetime(start_time)) or (
                    end_time and parse_datetime(tweet['time']) > parse_datetime(end_time))):
                continue
            for tag in tweet['tags']:
                if tag in target_tag or tweet['tags'][tag] in target_tag:
                    result_tag.update({tag: tweet['tags'][tag]})

            tweet['tags'] = result_tag
            if result_tag or not target_tag:
                new_tweet.append(tweet)
        results[user] = new_tweet

        results[user] = results[user][0:single]
        results[user].sort(key=lambda x: x.get('time'))
    results = dict(sorted(results.items(), key=lambda item: len(item[1]), reverse=True))

    timer = (time.time() - start_timer)

    make_this_point(len(results), timer)
    resp = init_http_success()
    resp['data'].update(results)
    return make_json_response(HttpResponse, resp)


if __name__ == '__main__':
    # import datetime
    #
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    # json_name = 'track\\{}\\{}\\{}\\{}\\{}\\{}\\{}.json'.format(None, 100, None, None, None, None, today)
    # print(json_name)
    # statistics_track_get(None)
    temp = []
    if temp:
        print(1)
