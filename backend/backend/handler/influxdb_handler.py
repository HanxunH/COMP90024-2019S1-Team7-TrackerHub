# -*- coding: utf-8 -*-

from influxdb import client

from backend.config.config import *


class InfluxDBHandler(object):

    def __init__(self, host=INFLUXDB_DOMAIN, port=INFLUXDB_PORT, username=INFLUXDB_USERNAME, password=INFLUXDB_PASSWORD,
                 database=INFLUXDB_DATABASE):
        self.client = client.InfluxDBClient(host=host, port=port, username=username, password=password)
        if database in self.list_database():
            self.client.switch_database(database)
        else:
            self.client.create_database(database)
            self.client.switch_database(database)

    def emit_one_record(self, data):
        return self.client.write_points([data])

    def make_point(self, key, action=None, method=None, error=None, prefix='', msg=None, value=1, **kwargs):
        point = {
            'measurement': prefix + '.' + key if prefix != '' else key,
            'tags': {},
            'fields': {
                'value': value
            }
        }
        if action:
            point['tags'].update(dict(action=action))
        if method:
            point['tags'].update(dict(method=method))
        if error:
            point['tags'].update(dict(error=error))
        if msg:
            point['fields'].update(dict(msg=msg))
        if value == 0:
            point['fields'].pop('value')
        if kwargs:
            for key in kwargs:
                point['fields'].update({key: kwargs[key]})
        return self.emit_one_record(point)

    def list_database(self):
        return self.client.get_list_database()


influxdb_handler = InfluxDBHandler()

if __name__ == '__main__':
    # data = 'api/tweet/pic,method=POST,1'
    # influxdb_handler.list_database()
    point = influxdb_handler.make_point('api/tweet/pic/', error=400, msg='not found')
    influxdb_handler.emit_one_record(point)
