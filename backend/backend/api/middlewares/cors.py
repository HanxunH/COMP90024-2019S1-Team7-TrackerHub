# coding: utf-8

from django.utils.deprecation import MiddlewareMixin


class CrosMeddleware(MiddlewareMixin):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Request-Methods'] = 'GET, OPTIONS, POST, PUT'
        response['Access-Control-Allow-Headers'] = 'Origin, X-Request-With, Content-Type, X-Api-Key, Accept, Accept-Language, Content-Language'
        response['Access-Control-Max-Age'] = 3628800

        return response
