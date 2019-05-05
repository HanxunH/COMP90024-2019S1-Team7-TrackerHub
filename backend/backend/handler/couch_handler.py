# -*- coding: utf-8 -*-

from couchdb.design import ViewDefinition
import couchdb
import logging

from backend.config.config import *


logger = logging.getLogger('django.debug')


class CouchDbHandler(object):

    load_balance_counter = None
    server = None
    database = dict()
    status = True

    def __init__(self, url=COUCHDB_URL, username=COUCHDB_USERNAME, password=COUCHDB_PASSWORD,
                 domain=COUCHDB_DOMAIN, ports=COUCHDB_PORTS):
        self.load_balance_counter = 0
        self.domain = domain
        self.ports = ports.__str__()

        try:
            self.server = couchdb.Server(url.format(username, password, domain, ports))
            logger.debug('CouchDB Connected Success: %s@%s:%s' % (username, domain, ports.__str__()))
        except Exception:
            logger.debug('CouchDB Connected Failed: %s@%s:%s' % (username, domain, ports.__str__()))
            self.status = False

    def get_database(self, _database):
        if not self.status:
            return None

        if _database in self.database:
            return self.database[_database]

        try:
            self.database.update({
                _database: self.server[_database]
            })
        except Exception:
            self.database.update({
                _database: self.server.create(_database)
            })
            logger.debug('CouchDB Database %s Created Success: %s:%s' % (_database, self.domain, self.ports))
        return self.database[_database]

    def make_views(self, database):
        pass



couch_db_handler = CouchDbHandler()

if __name__ == '__main__':

    tweet_database = couch_db_handler.get_database(COUCHDB_TWEET_DB)

    mango1 = {
        'selector': {
            '_id': {
                '$gt': None,
            },
            'process': 0
        },
        'limit': 100,
        'fields': ['_id', 'img_id'],
        'use_index': ['']
        # 'sort': [{'_id': 'asc'}]
    }

    my_map = '''
        function(doc) {
            if (doc.geo.length == 2) {
                emit(doc.user, doc.geo]);
            }
        }
    '''
    my_reduce = '''
        function (keys, values, rereduce) {
            var result = {};
            var temp = [];
            for (var value in values) {
                var t1 = values[value];
                for (var i = 0; i < t1.length; i+=2) {
                    if (temp.indexOf(t1[i]) > 0) {
                        temp[temp.indexOf(t1[i]) + 1] += 1; 
                    } else {
                        temp.push(t1[i]);
                        temp.push(t1[i+1]);
                    }
                }
            }
            return temp;
        }
    '''
    #

    options = dict(
        group=True,
        group_level=1,
        limit=100,
    )
    views = ViewDefinition('tracking', 'track', my_map, options=options)
    views.get_doc(tweet_database)
    views.sync(tweet_database)
    # design_doc = views.get_doc(tweet_database)
    # print(design_doc['views']['untrained']['map'])

    # tweets = tweet_database.find(mango1)
    # for tweet in tweets:
    #     print(tweet)
    # print(''.join(uuid1().__str__().split('-')))
    # index = tweet_database.index()
    # list(index)
    # index[''.join(uuid1().__str__().split('-')), 'process_is_zero'] = [{'process': 'asc'}]
    # index[''.join(uuid1().__str__().split('-')), 'date_index'] = [{'date': 'asc'}]
    # list(index)
    # tweets = tweet_database.view('_all_docs')
    # for tweet in tweets:
    #     print(tweet)

    docs = tweet_database.view('tracking/track')
    print(docs)
    for doc in docs:
        print(doc.id, doc.key, doc.value)

