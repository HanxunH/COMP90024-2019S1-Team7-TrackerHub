# -*- coding: utf-8 -*-

import couchdb
import logging

from backend.config.config import *
from backend.handler.influxdb_handler import influxdb_handler
from backend.common.couchdb_map import UNLEARNING, STATISTICS

logger = logging.getLogger('django.debug')


class CouchDbHandler(object):

    server = None
    database = dict()
    status = True

    def __init__(self, url=COUCHDB_URL, username=COUCHDB_USERNAME, password=COUCHDB_PASSWORD,
                 domain=COUCHDB_DOMAIN, ports=COUCHDB_PORTS):
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
            self.database[_database].save(UNLEARNING)
            self.database[_database].save(STATISTICS)
            logger.debug('CouchDB Database %s Created Success: %s:%s' % (_database, self.domain, self.ports))
        return self.database[_database]

    def make_views(self, database):
        pass


class CouchDBBalancer(object):

    servers = []
    databases = []
    domains = []
    balance = 0

    def __init__(self, domains=COUCHDB_DOMAINS):
        self.domains = domains
        for domain in domains:
            self.servers.append(CouchDbHandler(domain=domain))

    def connect_database(self, database):
        for server in self.servers:
            self.databases.append(server.get_database(database))

    def tick(self, action):
        self.balance += 1
        self.balance %= len(self.databases)
        influxdb_handler.make_point(key='Banlancer', action=action, method=self.domains[self.balance], prefix='CouchDB')

    def save(self, tweet):
        self.tick('save')
        return self.databases[self.balance].save(tweet)

    def get(self, id):
        self.tick('get')
        return self.databases[self.balance].get(id=id)

    def find(self, mango):
        self.tick('find')
        return self.databases[self.balance].find(mango)

    def get_current_database(self):
        self.tick('view')
        return self.databases[self.balance]

    def iterview(self, view, batch, wrapper=None):
        self.tick('view')
        return self.databases[self.balance].iterview(view, batch, wrapper)

    def compact(self):
        self.tick('compact')
        return self.databases[self.balance].compact()


couch_db_banlancer = CouchDBBalancer()
couch_db_banlancer.connect_database(COUCHDB_TWEET_DB)


if __name__ == '__main__':

    # mango = {
    #     'selector': {
    #         'geo': {
    #             '$ne': []
    #         }
    #     },
    #     'use_index': '_design/with_geo_and_tags',
    # }
    #
    # couch_db = couch_db_banlancer.view()
    # tweets = couch_db.view('with_geo_and_tags/with_geo_and_tags', stale='ok', limit=20)
    #
    # print(tweets)
    # for tweet in tweets:
    #     print(tweet)

    # tweet_database = couch_db_handler.get_database(COUCHDB_TWEET_DB)
    # index = tweet_database.index()
    # index[None, 'datetime'] = [{'date': 'asc'}]
    # list(index)

    tweet_database = couch_db_banlancer.get_current_database()
    # tweet_database.compact()
    tweets = tweet_database.view('statistics/user_geo', startkey='sunnyxcody', endkey='sunnyxcody', stale='ok', limit=200)
    tweets = [tweet.value for tweet in tweets]
    for tweet in tweets:
        print(tweet)



