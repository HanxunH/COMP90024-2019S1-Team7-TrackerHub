# coding: utf-8
"""
@Author: Lihuan Zhang

This files including the views that used to upload tweets and query unlearning tweet
"""

import ujson
import logging
import time

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from backend.handler.couch_handler import couch_db_banlancer
from backend.handler.influxdb_handler import influxdb_handler
from backend.common.utils import make_dict, init_http_not_found, init_http_success, init_http_bad_request, \
    check_api_key, make_json_response

tweet_couch_db = couch_db_banlancer
logger = logging.getLogger('django.debug')


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_router(request, resource=None, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """

    if request.method == 'POST':
        return tweet_post(request)
    elif request.method == 'GET' and resource:
        return tweet_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_trained_router(request, resource=None, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """

    if request.method == 'POST':
        return tweet_trained_post(request)
    elif request.method == 'GET':
        return tweet_trained_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_trained_text_router(request, resource=None, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """

    if request.method == 'POST':
        return tweet_trained_text_post(request)
    elif request.method == 'GET':
        return tweet_trained_text_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_trained_zone_router(request, resource=None, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """

    if request.method == 'POST':
        return tweet_trained_zone_post(request)
    elif request.method == 'GET':
        return tweet_trained_zone_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['POST'])
@check_api_key
def tweet_trained_zone_vic_router(request, resource=None, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """

    if request.method == 'POST':
        return tweet_trained_zone_vic_post(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def tweet_untrained_router(request, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """
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
    """
    A router used to control the permission and distribute request
    """
    resource = 100
    for arg in args:
        if isinstance(arg, dict):
            resource = arg.get('resource', 100)

    if request.method == 'GET':
        return tweet_untrained_text_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def tweet_untrained_zone_router(request, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """
    resource = 100
    for arg in args:
        if isinstance(arg, dict):
            resource = arg.get('resource', 100)

    if request.method == 'GET':
        return tweet_untrained_zone_get(request, resource)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def tweet_untrained_zone_vic_router(request, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """
    resource = 100
    for arg in args:
        if isinstance(arg, dict):
            resource = arg.get('resource', 100)

    if request.method == 'GET':
        return tweet_untrained_zone_vic_get(request, resource)
    return HttpResponseNotAllowed()


def tweet_post(request):
    """
    This views is used to receive crawler's tweet
    """
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
        # Process the datetime
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
    pass


def tweet_untrained_get(request, resource=100):
    """
    This views is used to return unlearnig tweet to client
    """
    start_timer = time.time()

    try:
        current_db = tweet_couch_db.get_current_database()
        tweets = current_db.view('unlearning/machine', limit=resource)
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/untrained/', method='GET', error=400, prefix='API')
        logger.error('Query Untrained Tweet Fail! %s', e)
        resp = init_http_not_found('Query Untrained Tweet Fail!')
        make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    for tweet in tweets:
        resp['data'].update({
            tweet.id: dict(
                img_id=tweet.value.get('img_id'),
                tags=tweet.value.get('tags', {}),
                model=tweet.value.get('model', {})
            )
        })

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/untrained/', method='GET', error='success', prefix='API',
                                tweet=len(resp['data']), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_post(request):
    """
    This views is used to receive the Machine Learning results from client
    """

    start_timer = time.time()

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

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/trained/', method='POST', error='success', prefix='API',
                                tweet=len(updated), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_get(request):
    """
    TODO: Implement
    """
    pass


def tweet_untrained_text_get(request, resource=100):
    """
    This views is used to return unlearnig tweet to client
    """

    start_timer = time.time()

    try:
        current_db = tweet_couch_db.get_current_database()
        tweets = current_db.view('unlearning/text', limit=resource)
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/untrained/text/', method='GET', error=400, prefix='API')
        logger.error('Query Untrained Tweet Fail! %s', e)
        resp = init_http_not_found('Query Untrained Tweet Fail!')
        make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    for tweet in tweets:
        resp['data'].update({
            tweet.id: dict(
                text=tweet.value.get('text'),
                tags={}
            )
        })

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/untrained/text/', method='GET', error='success', prefix='API',
                                tweet=len(resp['data']), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_text_get(request):
    """
    TODO: Implement for second training
    """
    pass


def tweet_trained_text_post(request):
    """
    This views is used to receive the Natural Language Process results from client
    """

    start_timer = time.time()

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

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/trained/text/', method='POST', error='success', prefix='API',
                                tweet=len(updated), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_untrained_zone_get(request, resource=100):
    """
    This views is used to return the tweet have not been located to client
    """

    start_timer = time.time()

    try:
        current_db = tweet_couch_db.get_current_database()
        tweets = current_db.view('unlearning/zone', limit=resource)
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/untrained/zone/', method='GET', error=400, prefix='API')
        logger.error('Query Untrained Tweet Fail! %s', e)
        resp = init_http_not_found('Query Untrained Tweet Fail!')
        make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    for tweet in tweets:
        resp['data'].update({
            tweet.id: dict(
                geo=tweet.value.get('geo', []),
                zone=None
            )
        })

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/untrained/zone/', method='GET', error='success', prefix='API',
                                tweet=len(resp['data']), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_untrained_zone_vic_get(request, resource=100):
    """
    This views is used to return the tweet have not been located to client
    """
    start_timer = time.time()

    try:
        current_db = tweet_couch_db.get_current_database()
        tweets = current_db.view('unlearning/vic_zone', limit=resource)
    except Exception as e:
        influxdb_handler.make_point(key='api/tweet/untrained/zone/vic/', method='GET', error=400, prefix='API')
        logger.error('Query Untrained Tweet Fail! %s', e)
        resp = init_http_not_found('Query Untrained Tweet Fail!')
        make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    for tweet in tweets:
        resp['data'].update({
            tweet.id: dict(
                geo=tweet.value.get('geo', []),
                zone=None
            )
        })

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/untrained/zone/vic/', method='GET', error='success', prefix='API',
                                tweet=len(resp['data']), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_zone_get(request):
    params = ujson.loads(request.body)


def tweet_trained_zone_post(request):
    """
    This views is used to received result from client to update the Melbourne zone of tweet
    """
    start_timer = time.time()

    results = ujson.loads(request.body)
    updated = dict()

    for result in results:
        try:
            _tweet = tweet_couch_db.get(id=result)
            tweet = dict([(k, v) for k, v in _tweet.items()])
            _now = timezone.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
            tweet.update(dict(
                last_update=_now,
                zone=results[result].get('zone', None)
            ))
            tweet_couch_db.save(tweet)

            updated.update({tweet['_id']: tweet['last_update']})

        except Exception as e:
            influxdb_handler.make_point(key='api/tweet/trained/zone/', method='POST', error=400, prefix='API')
            influxdb_handler.make_point(key='api/tweet/trained/zone/', method='POST', error='success', prefix='API',
                                        tweet=len(updated))
            logger.debug('Tweet post failed %s' % e)
            resp = init_http_bad_request('Tweet Attribute Required %s' % e)
            resp['data'] = updated
            return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'] = updated

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/trained/zone/', method='POST', error='success', prefix='API',
                                tweet=len(updated), timer=timer)
    return make_json_response(HttpResponse, resp)


def tweet_trained_zone_vic_post(request):
    """
    This views is used to received result from client to update the vic zone of tweet
    """
    start_timer = time.time()

    results = ujson.loads(request.body)
    updated = dict()

    for result in results:
        try:
            _tweet = tweet_couch_db.get(id=result)
            tweet = dict([(k, v) for k, v in _tweet.items()])
            _now = timezone.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
            tweet.update(dict(
                last_update=_now,
                vic_zone=results[result].get('zone', None)
            ))
            tweet_couch_db.save(tweet)

            updated.update({tweet['_id']: tweet['last_update']})

        except Exception as e:
            influxdb_handler.make_point(key='api/tweet/trained/zone/vic/', method='POST', error=400, prefix='API')
            influxdb_handler.make_point(key='api/tweet/trained/zone/vic/', method='POST', error='success', prefix='API',
                                        tweet=len(updated))
            logger.debug('Tweet post failed %s' % e)
            resp = init_http_bad_request('Tweet Attribute Required %s' % e)
            resp['data'] = updated
            return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'] = updated

    timer = (time.time() - start_timer)
    influxdb_handler.make_point(key='api/tweet/trained/zone/vic/', method='POST', error='success', prefix='API',
                                tweet=len(updated), timer=timer)
    return make_json_response(HttpResponse, resp)


if __name__ == '__main__':
    tweet_couch_db.compact()
