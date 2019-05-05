# -*- coding: utf-8 -*-


TRAINING_UNTRAIN_MAP = '''
        function(doc) {
            if ((doc.process == 0) && (doc.img_id.length != 0)) {
                emit(doc._id, doc.img_id);
            }
        }
    '''

TRACK_USER_MAP = '''
        function(doc) {
            if ((doc.get.length == 2)) {
                emit(doc.user, doc.geo)
            }
        }
    '''


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
        'limit': limit
    }

