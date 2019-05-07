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

    def make_views(self, database):
        pass



couch_db_handler = CouchDbHandler()

if __name__ == '__main__':

    tweet_database = couch_db_handler.get_database(COUCHDB_TWEET_DB)
    index = tweet_database.index()
    index[None, 'datetime'] = [{'date': 'asc'}]
    list(index)

