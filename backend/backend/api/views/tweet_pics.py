# coding: utf-8

import logging
from uuid import uuid1 as uuid

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse
from django.views.decorators.http import require_http_methods

from backend.handler.object_storage_handler import ObjectStorageHandler
from backend.common.utils import init_http_not_found, init_http_success, check_api_key, make_json_response
from backend.common.config import OBJECT_STORAGE_CONTAINER


logger = logging.getLogger('django.debug')


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_pic_router(request, *args, **kwargs):
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


def tweet_pic_post(request):
    try:
        file = request.FILES.get('file', None)
    except Exception as e:
        file = None
        logger.debug('No Attached File %s', e)

    if not file:
        resp = init_http_not_found('No Attach File')
        return make_json_response(HttpResponseNotFound, resp)

    uid = uuid()
    pic_id = ''.join(uid.__str__().split('-'))
    object_storage_handler = ObjectStorageHandler(OBJECT_STORAGE_CONTAINER)
    object_storage_handler.upload(pic_id + '.jpg', file)

    resp = init_http_success()
    resp['data'].update(dict(
        pic_id=pic_id
    ))

    return make_json_response(HttpResponse, resp)


def tweet_pic_list(request):

    def process(s):
        if 'name' in s:
            return s['name'].strip('.jpg')

    object_storage_handler = ObjectStorageHandler(OBJECT_STORAGE_CONTAINER)
    files = object_storage_handler.findall()
    pic_ids = map(process, files)

    resp = init_http_success()
    resp['data'].update(dict(
        pic_ids=pic_ids
    ))
    return make_json_response(HttpResponse, resp)


def tweet_pic_get(request, resource):
    resource = resource if '.jpg' in resource else resource + '.jpg'

    object_storage_handler = ObjectStorageHandler(OBJECT_STORAGE_CONTAINER)
    picture = object_storage_handler.download(resource)
    if not picture:
        resp = init_http_not_found('Object Storage Resource %s Not Found' % resource)
        return make_json_response(HttpResponseNotFound, resp)
    return FileResponse(picture, filename=resource, content_type='image/jpeg')