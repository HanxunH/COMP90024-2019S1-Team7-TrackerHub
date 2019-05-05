# -*- coding: utf-8 -*-

from influxdb import client


class InfluxDBHandler(object):

    def __init__(self, host='172.26.38.11', port=8086, username='admin', password='password', database='api_log'):
        self.client = client.InfluxDBClient(host=host, port=port, username=username, password=password)
        if database in self.list_database():
            self.client.switch_database(database)
        else:
            self.client.create_database(database)
            self.client.switch_database(database)

    def emit(self, api, method, count, prefix=None, func='log'):
        data = [{
            'measurement': 'api/tweet/pic',
            'tags': {'method': 'GET'},
            'fields': {
                'count': 1
            }
        }]
        self.client.write_points(data)

    def list_database(self):
        return self.client.get_list_database()


influxdb_handler = InfluxDBHandler()


if __name__ == '__main__':
    # data = 'api/tweet/pic,method=POST,1'
    # influxdb_handler.list_database()
    influxdb_handler.emit('api/tweet/pic/', 'POST', 1)
