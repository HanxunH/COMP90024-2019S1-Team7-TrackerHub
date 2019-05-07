# -*- coding: utf-8 -*-

import requests

from dockerManager import get_docker_manager
from config import *


def make_new_couchdb(domain, port):
    remote = get_docker_manager(domain, port)
    remote.remove_container('couchdb')
    remote.run(image='couchdb:2.3.0', name='couchdb', ports=COUCH_DB_PORTS, detach=True, environment=COUCH_DB_ENV, volumes=COUCH_DB_VOLUMES)
    remote.list()


def register_couchdb_node(master, node):
    master = master['domain']
    node = node['domain']

    url = 'http://{}:{}@{}:{}/_cluster_setup'.format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS.get('5984/tcp'))
    data = dict(
        action='enable_cluster',
        bind_address='0.0.0.0',
        username=COUCH_DB_USER,
        password=COUCH_DB_PASSWORD,
        port=COUCH_DB_PORTS.get('5984/tcp'),
        node_count=3,
        remote_node=node,
        remote_current_user=COUCH_DB_USER,
        remote_current_password=COUCH_DB_PASSWORD
    )
    headers = dict(
        contentType='application/json'
    )
    resp = requests.post(url, json=data, headers=headers)
    print(resp.status_code, resp.content)

    url2 = 'http://{}:{}@{}:{}/_cluster_setup'.format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS.get('5984/tcp'))
    data2 = dict(
        action='add_node',
        host=node,
        port=COUCH_DB_PORTS.get('5984/tcp'),
        username=COUCH_DB_USER,
        password=COUCH_DB_PASSWORD
    )
    resp = requests.post(url2, json=data2, headers=headers)
    print(resp.status_code, resp.content)


def finish_couchdb_cluster(master):
    master = master['domain']

    url = 'http://{}:{}@{}:{}/_cluster_setup'.format(COUCH_DB_USER, COUCH_DB_PASSWORD, master, COUCH_DB_PORTS.get('5984/tcp'))
    data = dict(
        action='finish_cluster'
    )
    header = dict(
        contentType='application/json'
    )
    resp = requests.post(url, json=data, headers=header)
    print(resp.status_code, resp.content)
