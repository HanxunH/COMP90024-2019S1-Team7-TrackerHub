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
    remote.run(image='tutum/influxdb:latest', name='influxdb', ports=INFLUXDB_PORTS, detach=True, environment=INFLUXDB_ENV, volumes=INFLUXDB_VOLUMES, restart_policy=RESTART)
    remote.list()


def make_new_grafana(domain, port):
    remote = get_docker_manager(domain, port)
    try:
        remote.remove_container('grafana')
    except Exception as e:
        print(e)
    remote.run(image='grafana/grafana:latest', name='grafana', ports=GRAFANA_PORTS, detach=True, environment=GRAFANA_ENV, volumes=GRAFANA_VOLUMES, restart_policy=RESTART)
    remote.list()


def make_new_cadvisor(domain, port, instance):
    remote = get_docker_manager(domain, port)
    try:
        remote.remove_container('cadvisor')
    except Exception as e:
        print(e)
    temp_command = CADVISOR_COMMAND
    temp_command[3] = instance
    remote.run(image='google/cadvisor:latest', name='cadvisor', ports=CADVISOR_PORTS, detach=True, volumes=CADVISOR_VOLUMES, command=temp_command)
    remote.list()


def make_new_smtp(domain, port):
    remote = get_docker_manager(domain, port)
    try:
        remote.remove_container('smtp')
    except Exception as e:
        print(e)
    # remote.run(image='namshi/smtp:latest', name='smtp', ports=SMTP_PORTS, detach=True, environment=SMTP_ENV)
    remote.list()
