# -*- coding: utf-8 -*-

from enum import Enum

HTTP_X_API_KEY = 'HTTP_X_API_KEY'
API_KEY = '227415ba68c811e9b1a48c8590c7151e'

COUCHDB_URL = 'http://{}:{}@{}:{}/'
COUCHDB_DOMAIN = '172.26.37.225'
COUCHDB_USERNAME = 'admin'
COUCHDB_PASSWORD = 'password'
COUCHDB_PORTS = 5984
COUCHDB_TWEET_DB = 'origin_tweet'
COUCHDB_TRACK_DB = 'track'
COUCHDB_TIME_DB = 'time_{}_{}_{}_{}_{}'

OBJECT_STORAGE_URL = 'https://swift.rc.nectar.org.au/v1/AUTH_0ca7fac1451c4f519376f20812279bfc'
OBJECT_STORAGE_CONTAINER = 'twitter_pic'

OS_AUTH_URL = 'https://keystone.rc.nectar.org.au:5000'
OS_TENANT_ID = 'unimelb-comp90024-group-7'
OS_USERNAME = 'lihuan.zhang@student.unimelb.edu.au'
OS_PASSWORD = 'NjNkMjk0Y2Y0MGYwYjlj'
OS_VERSION = '3'


class ErrorCode(Enum):
    success = 0
    not_found = 1
    unauthorized = 2


class ErrorMsg(Enum):
    success = 'success'
    not_found = 'resource not found'
    unauthorized = 'unauthorized access'
