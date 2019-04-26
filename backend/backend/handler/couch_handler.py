# -*- coding: utf-8 -*-

import couchdb

from backend.common.config import COUCHDB_URL, COUCHDB_PORTS, COUCHDB_DB


class CouchDbHandler(object):

    load_balance_counter = None
    server = None
    database = None

    def __init__(self, database, url=COUCHDB_URL, ports=COUCHDB_PORTS):
        self.load_balance_counter = 0
        self.server = couchdb.Server(url.format(ports[self.load_balance_counter % len(COUCHDB_PORTS)]))
        try:
            self.database = self.server[database]
        except Exception as e:
            print(e)
            self.database = self.server.create(database)

    def save(self):
        pass

    def create(self):
        pass

    def upload(self):
        pass

    def query(self):
        pass

    def delete(self):
        pass


couch_db_handler = CouchDbHandler(COUCHDB_DB)
