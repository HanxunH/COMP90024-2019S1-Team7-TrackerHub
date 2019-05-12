# coding: utf-8

import ujson
import logging
import time

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from backend.handler.couch_handler import couch_db_handler
from backend.handler.object_storage_handler import object_storage_handler
from backend.handler.influxdb_handler import influxdb_handler
from backend.common.utils import make_dict, init_http_not_found, init_http_success, init_http_bad_request, \
    check_api_key, make_json_response
from backend.common.couchdb_map import TRAINING_UNTRAINED_MANGO, TRAINING_UNTRAINED_TEXT_MANGO
from backend.config.config import COUCHDB_TWEET_DB

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


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_trained_router(request, resource=None, *args, **kwargs):
    if request.method == 'POST':
        return tweet_trained_post(request)
    elif request.method == 'GET':
        return tweet_trained_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_trained_text_router(request, resource=None, *args, **kwargs):
    if request.method == 'POST':
        return tweet_trained_text_post(request)
    elif request.method == 'GET':
        return tweet_trained_text_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def tweet_untrained_router(request, *args, **kwargs):
    resource = 100
    for arg in args:
        if isinstance(arg, dict):
            resource = arg.get('resource', 100)

    if request.method == 'GET':
        return tweet_untrained_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def tweet_untrained_text_router(request, *args, **kwargs):
    resource = 100
    for arg in args:
        if isinstance(arg, dict):
            resource = arg.get('resource', 100)

    if request.method == 'GET':
        return tweet_untrained_text_get(request, resource)
    return HttpResponseNotAllowed()


def tweet_post(request):
    try:
        keys = ['id', 'text', 'img_id', 'geo', 'date', 'user', 'hashtags']
        tweet = make_dict(keys, ujson.loads(request.body))
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/', method='POST', error=400, prefix='API', msg='error attribute')
        logger.debug('Insufficient Attributes [%s] %s' % (request.path, e))
        resp = init_http_not_found('Insufficient Attributes')
        return make_json_response(HttpResponseBadRequest, resp)

    if not isinstance(tweet['geo'], list) or not isinstance(tweet['hashtags'],
                                                            list or not isinstance(tweet['img_id'], list)):
        influxdb_handler.make_point(key='api/tweet/', method='POST', error=400, prefix='API', msg='error geo/img_id')
        resp = init_http_not_found('geo, hashtags, img_id must be LIST!')
        return make_json_response(HttpResponseBadRequest, resp)

    try:
        utc_tweet_time = parse_datetime(tweet['date']).astimezone(timezone.utc)
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/', method='POST', error=400, prefix='API', msg='error format time')
        logger.debug('Error Datetime Format [%s], %s' % (tweet['date'], e))
        resp = init_http_not_found('Error Datetime Format, follow \'%Y-%m-%d %H:%M:%S%z\'')
        return make_json_response(HttpResponseBadRequest, resp)

    if tweet['geo'] == ['']:
        tweet['geo'] = []

    tweet.update(dict(
        _id=tweet['id'],
        date=utc_tweet_time.strftime('%Y-%m-%d %H:%M:%S%z'),
        process=0,
        process_text=0,
        model={},
        tags={},
        last_update=timezone.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z'),
        text_update='',
        ml_update=''
    ))
    tweet.pop('id')

    try:
        tweet_id, rev = tweet_couch_db.save(tweet)
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/', method='POST', error=400, prefix='API', msg='existed')
        resp = init_http_not_found('Tweet Existed')
        return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'].update(dict(
        id=tweet_id,
        rev=rev
    ))
    influxdb_handler.make_point(key='api/tweet/', method='POST', error='success', prefix='API')
    return make_json_response(HttpResponse, resp)


def tweet_get(request, resource):
    key = ['']
    params = ujson.loads(request.body)

    pass


def tweet_untrained_get(request, resource=100):

    start_timer = time.time()

    try:
        tweets = tweet_couch_db.find(TRAINING_UNTRAINED_MANGO(resource))
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/untrained/', method='GET', error=400, prefix='API')
        logger.error('Query Untrained Tweet Fail! %s', e)
        resp = init_http_not_found('Query Untrained Tweet Fail!')
        make_json_response(HttpResponseBadRequest, resp)

    count = 0
    resp = init_http_success()
    for tweet in tweets:
        resp['data'].update({
            tweet.id: dict(
                img_id=tweet.get('img_id'),
                tags=tweet.get('tags'),
                model=tweet.get('model', {})
            )
        })
        count += 1

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/untrained/', method='GET', error='success', prefix='API', tweet=count, timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_post(request):
    results = ujson.loads(request.body)
    updated = dict()

    for result in results:
        try:
            _tweet = tweet_couch_db.get(id=result)
            tweet = dict([(k, v) for k, v in _tweet.items() if k not in ('_id', '_rev')])
            tweet.update(dict(
                _id=_tweet.id,
                _rev=_tweet.rev
            ))

            tweet['tags'].update(results[result]['tags'])
            tweet['model'] = results[result]['model']
            _now = timezone.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
            tweet.update(dict(
                ml_update=_now,
                last_update=_now,
                process=tweet['process'] + 1
            ))
            tweet_couch_db.save(tweet)

            updated.update({tweet['_id']: tweet['ml_update']})

        except Exception as e:
            influxdb_handler.make_point(key='api/tweet/trained/', method='POST', error=400, prefix='API')
            influxdb_handler.make_point(key='api/tweet/trained/', method='POST', error='success', prefix='API',
                                        tweet=len(updated))
            logger.debug('Tweet post failed %s' % e)
            resp = init_http_bad_request('Tweet Attribute Required %s' % e)
            resp['data'] = updated
            return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'] = updated
    influxdb_handler.make_point(key='api/tweet/trained/', method='POST', error='success', prefix='API',
                                tweet=len(updated))
    return make_json_response(HttpResponse, resp)


def tweet_trained_get(request):
    params = ujson.loads(request.body)


def tweet_untrained_text_get(request, resource=100):

    start_timer = time.time()

    try:
        tweets = tweet_couch_db.find(TRAINING_UNTRAINED_TEXT_MANGO(resource))
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/untrained/text/', method='GET', error=400, prefix='API')
        logger.error('Query Untrained Tweet Fail! %s', e)
        resp = init_http_not_found('Query Untrained Tweet Fail!')
        make_json_response(HttpResponseBadRequest, resp)

    count = 0
    resp = init_http_success()
    for tweet in tweets:
        resp['data'].update({
            tweet.id: dict(
                text=tweet.get('text'),
                tags=tweet.get('tags').get('text', {}),
            )
        })
        count += 1

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/untrained/text/', method='GET', error='success', prefix='API', tweet=count, timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_text_get(request):
    params = ujson.loads(request.body)


def tweet_trained_text_post(request):
    results = ujson.loads(request.body)
    updated = dict()

    for result in results:
        try:
            _tweet = tweet_couch_db.get(id=result)
            tweet = dict([(k, v) for k, v in _tweet.items() if k not in ('_id', '_rev')])
            tweet.update(dict(
                _id=_tweet.id,
                _rev=_tweet.rev
            ))

            tweet['tags'].update(results[result]['tags'])
            _now = timezone.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
            tweet.update(dict(
                text_update=_now,
                last_update=_now,
                process_text=tweet['process_text'] + 1
            ))
            tweet_couch_db.save(tweet)

            updated.update({tweet['_id']: tweet['text_update']})

        except Exception as e:
            influxdb_handler.make_point(key='api/tweet/trained/text/', method='POST', error=400, prefix='API')
            influxdb_handler.make_point(key='api/tweet/trained/text/', method='POST', error='success', prefix='API',
                                        tweet=len(updated))
            logger.debug('Tweet post failed %s' % e)
            resp = init_http_bad_request('Tweet Attribute Required %s' % e)
            resp['data'] = updated
            return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'] = updated
    influxdb_handler.make_point(key='api/tweet/trained/text/', method='POST', error='success', prefix='API',
                                tweet=len(updated))
    return make_json_response(HttpResponse, resp)


if __name__ == '__main__':
    # mango = {
    #     'selector': {
    #         'text_update': {
    #             '$exists': False
    #         }
    #     },
    #     'limit': 15000
    # }
    # tweets = tweet_couch_db.find(mango)
    # for tweet in tweets:
    #     newTweet = dict([(k, v) for k, v in tweet.items() if k not in ('_id', '_rev')])
    #     print(newTweet)
    #     newTweet.update(dict(
    #         _id=tweet.id,
    #         _rev=tweet.rev,
    #         text_update=newTweet.get('text_updated', ''),
    #         ml_update=newTweet.get('lm_updated', ''),
    #         last_update=newTweet.get('last_updated', newTweet.get('last_update'))
    #     ))
    #     if 'text_updated' in newTweet:
    #         newTweet.pop('text_updated')
    #     if 'ml_updated' in newTweet:
    #         newTweet.pop('ml_updated')
    #     if 'last_updated' in newTweet:
    #         newTweet.pop('last_updated')
    #     print(newTweet)
    #     # tweet_couch_db.delete(newTweet)
    #     tweet_couch_db.save(newTweet)
    # tweet_couch_db.compact()
    # pass
    import datetime
    import pytz

    mango = {
        'selector': {
            'img_id': {
                '$ne': []
            },
            'last_update': {
                '$lt': (datetime.datetime.now().astimezone(pytz.utc) - datetime.timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S%z')
            },
            'process': {
                '$eq': 0
            }
        },
        'limit': 400000,
        # 'skip': 1000,
    }

    tweets = tweet_couch_db.find(mango)
    for tweet in tweets:
        newTweet = dict([(k, v) for k, v in tweet.items() if k not in ('_id', '_rev')])
        newTweet.update(dict(
            _id=tweet.id,
            _rev=tweet.rev,
        ))
        for img in newTweet['img_id']:
            try:
                picture = object_storage_handler.download(img + '.jpg')
            except Exception as e:
                object_storage_handler.reconnect()
                picture = object_storage_handler.download(img + '.jpg')

            if not picture:
                newTweet['img_id'].remove(img)
        newTweet['last_update'] = datetime.datetime.now().astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S%z')
        try:
            tweet_couch_db.save(newTweet)
        except Exception:
            continue
    tweet_couch_db.compact()
