# coding: utf-8

import ujson
import logging

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from backend.handler.couch_handler import couch_db_handler
from backend.common.utils import make_dict, init_http_not_found, init_http_success, check_api_key, make_json_response
from backend.common.config import COUCHDB_TWEET_DB, COUCHDB_TRACK_DB, COUCHDB_TIME_DB


tweet_couch_db = couch_db_handler.get_database(COUCHDB_TWEET_DB)
logger = logging.getLogger('django.debug')


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
        logger.debug('Insufficient Attributes [%s] %s' % (request.path, e))
        resp = init_http_not_found('Insufficient Attributes')
        return make_json_response(HttpResponseNotFound, resp)

    try:
        utc_tweet_time = parse_datetime(tweet['date']).astimezone(timezone.utc)
    except Exception as e:
        logger.debug('Error Datetime Format [%s], %s' % (tweet['date'], e))
        resp = init_http_not_found('Error Datetime Format, follow \'%Y-%m-%d %H:%M:%S%z\'')
        return make_json_response(HttpResponseNotFound, resp)
    
    tweet.update(dict(
        _id=tweet['id'],
        date=utc_tweet_time.strftime('%Y-%m-%d %H:%M:%S%z'),
        process=0,
        tags=[],
        last_update=timezone.datetime.utcnow().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
    ))
    tweet.pop('id')

    try:
        tweet_id, rev = tweet_couch_db.save(tweet)
    except Exception as e:
        resp = init_http_not_found('Tweet Existed')
        return make_json_response(HttpResponseNotFound, resp)

    resp = init_http_success()
    resp['data'].update(dict(
        id=tweet_id,
        rev=rev
    ))
    return make_json_response(HttpResponse, resp)


def tweet_get(request, resource):
    pass
