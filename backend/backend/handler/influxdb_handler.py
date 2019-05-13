# -*- coding: utf-8 -*-
"""
@Author: Lihuan Zhang

This handler is used to operate InfluxDB
"""

from influxdb import client

from backend.config.config import *


class InfluxDBHandler(object):
    """
    This handler is used to make a record on influxdb
    """
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
        """
        Make one record in the influxdb with parameters
        """
        point = {
            'measurement': prefix + '.' + key if prefix != '' else key,
            'tags': {},
            'fields': {
                'value': value
            }
        }
        point['tags'].update(dict(action=action)) if action else None
        point['tags'].update(dict(method=method)) if method else None
        point['tags'].update(dict(error=error)) if error else None
        point['fields'].update(dict(msg=msg)) if msg else None
        point['fields'].pop('value') if value == 0 else None
        if kwargs:
            for key in kwargs:
                point['fields'].update({key: kwargs[key]})
        return self.emit_one_record(point)

    def list_database(self):
        return self.client.get_list_database()


influxdb_handler = InfluxDBHandler()

if __name__ == '__main__':
    point = influxdb_handler.make_point('api/tweet/pic/', error=400, msg='not found')
    influxdb_handler.emit_one_record(point)
