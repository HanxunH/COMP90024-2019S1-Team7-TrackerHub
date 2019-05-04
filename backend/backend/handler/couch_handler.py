# -*- coding: utf-8 -*-

import couchdb
import logging

from backend.common.config import *


logger = logging.getLogger('django.debug')


class CouchDbHandler(object):

    load_balance_counter = None
    server = None
    database = None

    def __init__(self, database, url=COUCHDB_URL, username=COUCHDB_USERNAME, password=COUCHDB_PASSWORD,
                 domain=COUCHDB_DOMAIN, ports=COUCHDB_PORTS):
        self.load_balance_counter = 0
        try:
            self.server = couchdb.Server(url.format(username, password, domain, ports[self.load_balance_counter % len(COUCHDB_PORTS)]))
        except Exception:
            logger.debug('CouchDB Connected Failed: %s@%s:%s' % (username, domain, ports.__str__()))
            return

        try:
            self.database = self.server[database]
        except Exception:
            self.database = self.server.create(database)
        logger.debug('CouchDB Connected Success: %s@%s:%s Collection Used: %s' % (username, domain, ports.__str__(), database))

    def save(self):
        pass

    def create(self, doc):
        resp = self.database.update(doc)
        return resp

    def update(self):
        pass

    def query(self):
        pass

    def delete(self):
        pass


class GetCouchDbHandlers(object):
    couch_db_handler = dict()

    @classmethod
    def get_couch_db_handler(cls, database):
        if database not in cls.couch_db_handler:
            try:
                cls.couch_db_handler.update({database: CouchDbHandler(COUCHDB_DB)})
            except Exception:
                logger.debug('CouchDB Connected Failed! Database: %s' % database)
                cls.couch_db_handler.update({database: None})
        return cls.couch_db_handler[database]


couch_db_handler = GetCouchDbHandlers.get_couch_db_handler(COUCHDB_DB)


if __name__ == '__main__':
    document = [dict(
        flag='test',
        index='test1',
    ), dict(
        flag='nottest',
        index='hello',
    )]
    couch_db_handler = GetCouchDbHandlers.get_couch_db_handler(COUCHDB_DB)
    print(couch_db_handler)
    if couch_db_handler:
        print(couch_db_handler.create(document))
