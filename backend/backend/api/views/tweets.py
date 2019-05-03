# coding: utf-8

import ujson
import math

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from backend.handler.couch_handler import couch_db_handler
from backend.common.utils import make_dict, init_http_not_found, init_http_success, check_api_key, make_json_response
from backend.common.config import COUCHDB_TWEET_DB, COUCHDB_TRACK_DB, COUCHDB_TIME_DB


tweet_couch_db = couch_db_handler.get_database(COUCHDB_TWEET_DB)


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_router(request, resource=None, *args, **kwargs):
    if request.method == 'POST':
        return tweet_post(request)
    elif request.method == 'GET' and resource:
        return tweet_get(request, resource)
    return HttpResponseNotAllowed()


def tweet_post(request):
    try:
        keys = ['id', 'text', 'image_urls', 'img_id', 'geo', 'date', 'user', 'hashtag']
        tweet = make_dict(keys, ujson.loads(request.body))
    except Exception as e:
        print(e)
        resp = init_http_not_found('Not Sufficient Attributes')
        return make_json_response(HttpResponseNotFound, resp)

    utc_tweet_time = timezone.datetime.strptime(tweet['date'], '%Y-%m-%d %H:%M:%S%z').astimezone(timezone.utc)
    tweet.update(dict(
        _id=tweet['id'],
        date=utc_tweet_time.strftime('%Y-%m-%d %H:%M:%S%z'),
        tags=[],
        last_update=timezone.datetime.utcnow().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
    ))
    tweet.pop('id')
    time_tweet_record = dict(
        _id=tweet['_id']
    )
    minute = math.floor(utc_tweet_time.minute / 15) * 15
    time_couch_db = couch_db_handler.get_database(COUCHDB_TIME_DB.format(utc_tweet_time.year, utc_tweet_time.month,
                                                                         utc_tweet_time.day, utc_tweet_time.hour,
                                                                         minute))
    try:
        id, rev = tweet_couch_db.save(tweet)
        time_couch_db.save(time_tweet_record)
    except Exception as e:
        print(e)
        resp = init_http_not_found('Tweet Existed')
        return make_json_response(HttpResponseNotFound, resp)

    resp = init_http_success()
    resp['data'].update(dict(
        id=id,
        rev=rev
    ))
    return make_json_response(HttpResponse, resp)


def tweet_get(request, resource):
    pass
