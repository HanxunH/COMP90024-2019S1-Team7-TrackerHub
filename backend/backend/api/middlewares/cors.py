# coding: utf-8

from django.utils.deprecation import MiddlewareMixin


class CrosMeddleware(MiddlewareMixin):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        return response
