# -*- coding: utf-8 -*-

import requests

from dockerManager import get_docker_manager
from config import *


def make_new_influxdb(domain, port):
    remote = get_docker_manager(domain, port)
    try:
        remote.remove_container('influxdb')
    except Exception as e:
        print(e)
    remote.run(image='tutum/influxdb:latest', name='influxdb', ports=INFLUXDB_PORTS, detach=True, environment=INFLUXDB_ENV, volumes=INFLUXDB_VOLUMES)
    remote.list()


def make_new_grafana(domain, port):
    remote = get_docker_manager(domain, port)
    try:
        remote.remove_container('influxdb')
    except Exception as e:
        print(e)
    remote.run(image='influxdb', name='influxdb', ports=INFLUXDB_PORTS, detach=True, volumes=INFLUXDB_VOLUMES)
    remote.list()