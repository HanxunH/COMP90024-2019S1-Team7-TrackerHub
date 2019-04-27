# -*- coding: utf-8 -*-

import ujson
from uuid import uuid1 as uuid
from swiftclient.exceptions import ClientException

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound, FileResponse
from django.views.decorators.http import require_http_methods

from backend.handler.object_storage_handler import object_storage_handler
from backend.common.utils import init_http_not_found, check_api_key


@require_http_methods(['POST', 'GET'])
def tweet_pic_router(request, resource=None, *args, **kwargs):
    if request.method == 'POST':
        return tweet_pic_post(request)
    elif request.method == 'GET':
        return tweet_pic_get(request, resource)
    return HttpResponseNotAllowed()


def tweet_pic_post(request, *args, **kwargs):
    uid = uuid()
    file_name = uid.__str__() + '.jpg'
    picture = request.FILES.get('picture')
    hash_code = object_storage_handler.upload(file_name, picture)
    return HttpResponse()


@check_api_key
def tweet_pic_get(request, resource=None, *args, **kwargs):
    if not resource:
        return HttpResponseNotFound()
    resource = resource[0]
    resource = resource if '.jpg' in resource else resource + '.jpg'

    picture = object_storage_handler.download(resource)
    if not picture:
        resp = init_http_not_found('Object Storage Resource %s Not Found' % resource)
        return HttpResponseNotFound(ujson.dumps(resp), content_type='application/json')
    print(picture)
    return FileResponse(picture, content_type='image/jpeg')


def tweet_storage(request, *args, **kwargs):
    pass
