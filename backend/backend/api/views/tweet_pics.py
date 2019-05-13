# coding: utf-8
"""
@Author: Lihuan Zhang

This files including the views that used to receive picture and download picture
"""

import logging
from uuid import uuid1 as uuid

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from backend.handler.object_storage_handler import object_storage_handler, json_storage_handler
from backend.handler.influxdb_handler import influxdb_handler
from backend.common.utils import init_http_not_found, init_http_success, check_api_key, make_json_response

logger = logging.getLogger('django.debug')


@require_http_methods(['POST', 'GET'])
def tweet_pic_router(request, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """
    resource = None
    for arg in args:
        if isinstance(arg, dict):
            resource = arg.get('resource', None)

    if request.method == 'POST':
        return tweet_pic_post(request)
    elif request.method == 'GET' and resource:
        return tweet_pic_get(request, resource)
    elif request.method == 'GET':
        return tweet_pic_list(request)
    return HttpResponseNotAllowed()


@require_http_methods(['GET'])
def geo_file_router(request, resource=None, *args, **kwargs):
    """
    A router used to control the permission and distribute request
    """

    if request.method == 'GET' and resource:
        return geo_file_get(request, resource)
    return HttpResponseNotAllowed()


def tweet_pic_post(request):
    try:
        file = request.FILES.get('file', None)
    except Exception as e:
        file = None
        logger.debug('No Attached File %s', e)

    if not file:
        influxdb_handler.make_point(key='api/tweet/pic/', prefix='API', method='POST', error=400, msg='no attach pic')
        resp = init_http_not_found('No Attach File')
        return make_json_response(HttpResponseBadRequest, resp)

    uid = uuid()
    pic_id = ''.join(uid.__str__().split('-'))

    try:
        object_storage_handler.upload(pic_id + '.jpg', file)
    except Exception as e:
        tweet_pic_reconnect(e)
        object_storage_handler.upload(pic_id + '.jpg', file)

    try:
        pic = object_storage_handler.download(pic_id + '.jpg')
    except Exception as e:
        tweet_pic_reconnect(e)
        pic = object_storage_handler.download(pic_id + '.jpg')

    if not pic:
        influxdb_handler.make_point(key='api/tweet/pic/', prefix='API', method='POST', error=400)
        resp = init_http_not_found('Pic Upload Fail')
        return make_json_response(HttpResponseBadRequest, resp)

    resp = init_http_success()
    resp['data'].update(dict(
        pic_id=pic_id
    ))
    influxdb_handler.make_point(key='api/tweet/pic/', prefix='API', method='POST', error='success')
    return make_json_response(HttpResponse, resp)


def tweet_pic_list(request):
    def process(s):
        if 'name' in s:
            return s['name'].strip('.jpg')

    try:
        files = object_storage_handler.findall()
    except Exception as e:
        tweet_pic_reconnect(e)
        files = object_storage_handler.findall()

    pic_ids = map(process, files)

    resp = init_http_success()
    resp['data'].update(dict(
        pic_ids=pic_ids
    ))
    influxdb_handler.make_point(key='api/tweet/pic/', prefix='API', method='GET', error='success')
    return make_json_response(HttpResponse, resp)


def tweet_pic_get(request, resource):

    resource = resource if '.jpg' in resource else resource + '.jpg'

    try:
        picture = object_storage_handler.download(resource)
    except Exception as e:
        tweet_pic_reconnect(e)
        picture = object_storage_handler.download(resource)

    if not picture:
        influxdb_handler.make_point(key='api/tweet/pic/:pic_id/', prefix='API', error=404, method='GET',
                                    msg='pic not found')
        resp = init_http_not_found('Object Storage Resource %s Not Found' % resource)
        return make_json_response(HttpResponseNotFound, resp)

    influxdb_handler.make_point(key='api/tweet/pic/:pic_id/', prefix='API', method='GET', error='success')
    return FileResponse(picture, filename=resource, content_type='image/jpeg')


def geo_file_get(request, resource):

    resource = resource if '.json' in resource else resource + '.json'

    try:
        file = json_storage_handler.download(resource)
    except Exception as e:
        json_storage_handler.reconnect()
        file = json_storage_handler.download(resource)

    if not file:
        influxdb_handler.make_point(key='api/statistics/file/:file/', prefix='API', error=404, method='GET',
                                    msg='pic not found')
        resp = init_http_not_found('Object Storage Resource %s Not Found' % resource)
        return make_json_response(HttpResponseNotFound, resp)

    influxdb_handler.make_point(key='api/statistics/file/:file/', prefix='API', method='GET', error='success')
    return FileResponse(file, filename=resource)


def tweet_pic_reconnect(exception):
    logger.debug('Reconnect Object Storage: %s', exception)
    influxdb_handler.make_point(key='Operate', prefix='ObjectStorage', action='Reconnect')
    object_storage_handler.reconnect()
