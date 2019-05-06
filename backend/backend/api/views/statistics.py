# coding: utf-8

import logging
import ujson
from shapely.geometry import shape, point

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from backend.handler.couch_handler import CouchDbHandler
from backend.handler.influxdb_handler import influxdb_handler
from backend.common.couchdb_map import STATISTICS_TIME_MANGO
from backend.common.utils import make_dict, init_http_not_found, init_http_success, check_api_key, make_json_response
from backend.config.config import COUCHDB_TWEET_DB


logger = logging.getLogger('django.debug')


@require_http_methods(['GET'])
@check_api_key
def statistics_time_router(request, *args, **kwargs):
    if request.method == 'GET':
        return statistics_time_get(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
@check_api_key
def statistics_track_router(request, *args, **kwargs):
    user_id = None
    for arg in args:
        if isinstance(arg, dict):
            user_id = arg.get('user_id', None)

    if request.method == 'GET':
        return statistics_track_get(request, user_id)
    return HttpResponseNotAllowed()


def statistics_time_get(request):
    key = ['start_time', 'end_time', 'tags']
    content = ujson.loads(request.body)
    content = make_dict(key, content)

    if 'start_time' in content:
        start_time = parse_datetime(content['start_time']).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')
    if 'end_time' in content:
        end_time = parse_datetime(content['end_time']).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')




def upload_statistics_file():
    pass


def down_statistics_file(request):
    pass


def statistics_track_get(request, user_id=None):

    if user_id:
        mango = {
            'selector': {
                'process': 0,
                '$not': {
                    'img_id': []
                }
            },
            'fields': ['_id', 'img_id', 'tags', 'model'],
            'use_index': 'json:process',
            'limit': 100
        }


