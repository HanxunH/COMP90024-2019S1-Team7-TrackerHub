# -*- coding: utf-8 -*-

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


couch_db_handler = CouchDbHandler()

if __name__ == '__main__':
    from uuid import uuid1
    # from couchdb import Document
    #
    # class myDoc(Document):
    #     @property
    #     def img_id(self):
    #         """The document ID.
    #
    #         :rtype: basestring
    #         """
    #         return self.get('img_id')


    tweet_database = couch_db_handler.get_database(COUCHDB_TWEET_DB)
    mango1 = {
        'selector': {
            '_id': {
                '$gt': None,
            },
            # 'process': 0
        },
        'fields': ['_id', 'img_id'],
        'sort': [{'_id': 'desc'}]
    }
    mango2 = {
        'selector': {
            '_id': {
                '$gt': None,
                # '$gt': '2016-01-01 00:00:00+0000',
                # '$lt': '2019-01-01 00:00:00+0000'
                # '$in': ['2017-01-01 00:00:00+0000', '2019-01-01 00:00:00+0000']
            }
        },
        'fields': ['_id', 'date'],
        # 'sort': ['_id:string']
    }
    # tweets = tweet_database.find(mango1, myDoc)

    # print(''.join(uuid1().__str__().split('-')))
    index = tweet_database.index()
    list(index)
    index[''.join(uuid1().__str__().split('-')), 'process_is_zero'] = [{'process': 'asc'}]
    index[''.join(uuid1().__str__().split('-')), 'date_index'] = [{'date': 'asc'}]
    list(index)
    # tweets = tweet_database.view('_all_docs')
    # for tweet in tweets:
    #     print(tweet)
