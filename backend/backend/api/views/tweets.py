# -*- coding: utf-8 -*-

import ujson
from uuid import uuid1 as uuid

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse
from django.views.decorators.http import require_http_methods

from backend.handler.object_storage_handler import object_storage_handler
from backend.common.utils import init_http_not_found, init_http_success, check_api_key, make_json_response


@require_http_methods(['POST', 'GET'])
@check_api_key
def tweet_pic_router(request, resource=None, *args, **kwargs):
    if request.method == 'POST':
        return tweet_pic_post(request)
    elif request.method == 'GET' and resource:
        return tweet_pic_get(request, resource)
    elif request.method == 'GET':
        return tweet_pic_list(request)
    return HttpResponseNotAllowed()


def tweet_pic_post(request):
    file = request.FILES.get('file', None)
    if not file:
        resp = init_http_not_found('No Attach File')
        return make_json_response(HttpResponseNotFound, resp)

    uid = uuid()
    file_name = ''.join(uid.__str__().split('-'))
    object_storage_handler.upload(file_name + '.jpg', file)

    resp = init_http_success()
    resp['data'].update(dict(
        filename=file_name
    ))

    return make_json_response(HttpResponse, resp)


def tweet_pic_list(request):

    def process(s):
        if 'name' in s:
            return s['name'].strip('.jpg')

    files = object_storage_handler.findall()
    files = map(process, files)

    resp = init_http_success()
    resp['data'].update(dict(
        pics=files
    ))
    return make_json_response(HttpResponse, resp)


def tweet_pic_get(request, resource):
    if isinstance(resource, tuple):
        resource = resource[0]
    resource = resource if '.jpg' in resource else resource + '.jpg'

    picture = object_storage_handler.download(resource)
    if not picture:
        resp = init_http_not_found('Object Storage Resource %s Not Found' % resource)
        return make_json_response(HttpResponseNotFound, resp)
    return FileResponse(picture, filename=resource, content_type='image/jpeg')


def tweet_storage(request):
    pass
