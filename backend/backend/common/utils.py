# coding: utf-8

import logging
import ujson
import json
import datetime

from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from backend.common.config import ErrorCode, ErrorMsg
from backend.config.config import HTTP_X_API_KEY, API_KEY


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


def str_to_str_datetime_utc(time):
    return parse_datetime(time).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')


def make_dict(keys, kwargs):
    result = dict()
    for key in kwargs.keys():
        if key in keys:
            result.update({key: kwargs[key]})
    return result


def check_api_key(func):
    def wrapper(request, *args, **kwargs):
        api_key = request.META.get(HTTP_X_API_KEY, None)
        if api_key == API_KEY:
            return func(request, args, kwargs)
        else:
            logging.warning('Unpermitted Access To \'%s\'', request.path_info)
            resp = init_http_unauthorized('Unpermitted Access To \'%s\'' % request.path_info)
            return make_json_response(HttpResponseForbidden, resp)
    return wrapper


def make_json_response(func=HttpResponse, resp=None):
    return func(ujson.dumps(resp), content_type='application/json')


def init_http_response(err_code, err_msg):
    return dict(
        err_code=err_code,
        err_msg=err_msg,
        data=dict(),
    )


def init_http_success(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.success.value, ErrorMsg.success.value)
    return init_http_response(ErrorCode.success.value, err_msg)


def init_http_not_found(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.not_found.value, ErrorMsg.not_found.value)
    return init_http_response(ErrorCode.not_found.value, err_msg)


def init_http_bad_request(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.bad_request.value, ErrorMsg.not_found.value)
    return init_http_response(ErrorCode.bad_request.value, err_msg)


def init_http_unauthorized(err_msg=None):
    if not err_msg:
        return init_http_response(ErrorCode.unauthorized.value, ErrorMsg.unauthorized.value)
    return init_http_response(ErrorCode.unauthorized.value, err_msg)