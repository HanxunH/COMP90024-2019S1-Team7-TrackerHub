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