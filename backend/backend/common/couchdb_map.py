# -*- coding: utf-8 -*-


def TRAINING_UNTRAINED_MANGO(limit=100):
    return {
        'selector': {
            'process': 0,
            '$not': {
                'img_id': []
            }
        },
        'fields': ['_id', 'img_id', 'tags', 'model'],
        'use_index': 'json:process',
        'limit': limit
    }


def TRAINING_UNTRAINED_TEXT_MANGO(limit=100):
    return {
        'selector': {
            'process_text': 0,
        },
        'fields': ['_id', 'text', 'tags'],
        'use_index': 'json:process-text-index',
        'limit': limit
    }


def STATISTICS_TIME_MANGO(start_time=None, end_time=None, porn=None, food=None):
    mango = {
        'selector': {
            'date': {
                '$gt': start_time,
                '$lt': end_time
            },
            '$or': [
                {
                    'tags': {

                    }
                }
            ]
        }
    }


    mango = {
        'selector': {
            '$or': [{
                '$and': [
                    {
                        'tags': {
                            '$ne': {}
                        }
                    },
                    {
                        'tags': {
                            'netural'
                        }
                    }
                ],
                'tags': {
                    '$ne': {}
                }}, {
                'geo': {
                    '$ne': []
            }}]
        },
        'fields': ['_id', 'text', 'tags'],
        'limit': 100,
        'use_index': 'json:date-index'
    }
    if start_time or end_time:
        mango['selector'].update({'date': {}})
    if start_time:
        mango['selector']['date'].update({'$gt': start_time})
    if end_time:
        mango['selector']['date'].update({'$lt': end_time})
    if porn or food:
        mango['selector'].update('tags')


def statistics_track_random(start_time=None, end_time=None, user_id=None, limit=10000, skip=0):
    mango = {
        'selector': {
            'geo': {
                '$ne': []
            }
        },
        'use_index': 'json:geo-index',
        'limit': limit,
        'skip': skip
    }

    if start_time or end_time:
        mango['selector'].update(dict(date={}))
        mango['selector']['date'].update({'$gte': start_time}) if start_time else None
        mango['selector']['date'].update({'$lte': end_time}) if end_time else None
        mango.update(dict(use_index='json:date-index'))
    if user_id:
        mango['selector'].update(dict(user=user_id))
        mango.update(dict(use_index='json:user-date-index'))

    return mango