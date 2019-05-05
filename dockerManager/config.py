# -*- coding: utf-8 -*-

DOCKER_DOMAIN = {
    'instance1': dict(
        domain='172.26.37.225',
        port=8866
    ),
    'instance2': dict(
        domain='172.26.38.110',
        port=8866
    ),
    'instance3': dict(
        domain='172.26.38.1',
        port=8866
    ),
}

COUCH_DB_PORTS = {
    '5984/tcp': 5984,
    '5896/tcp': 5986,
    '4369/tcp': 4369,
    '9100/tcp': 9100,
}

COUCH_DB_VOLUMES = {
    '/home/ubuntu/couchdb/etc/docker.ini': {'bind': '/opt/couchdb/etc/local.d/docker.ini', 'mode': 'rw'},
    '/home/ubuntu/couchdb/etc/vm.args': {'bind': '/opt/couchdb/etc/vm.args', 'mode': 'rw'},
    '/home/ubuntu/couchdb/etc/default.ini': {'bind': '/opt/couchdb/etc/default.ini', 'mode': 'rw'},
    '/data/': {'bind': '/opt/couchdb/data', 'mode': 'rw'}
}

COUCH_DB_USER = 'GROUP7'
COUCH_DB_PASSWORD = 'group7'
COUCH_DB_ENV = ['COUCHDB_USER={}'.format(COUCH_DB_USER), 'COUCHDB_PASSWORD={}'.format(COUCH_DB_PASSWORD)]

DJANGO_PORTS = {
    '8080/tcp': 8080,
    '80/tcp': 8081,
}

DJANGO_VOLUMES = {
    '/home/ubuntu/COMP90024/backend/': {'bind': ''}
}

NGINX_PORTS = {
    '80/tcp': 8088
}
