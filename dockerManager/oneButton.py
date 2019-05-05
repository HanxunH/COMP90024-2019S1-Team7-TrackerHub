# -*- coding: utf-8 -*-

import threading

from dockerSetCouchDBCluster import *


if __name__ == '__main__':

    threads = []
    for instance in DOCKER_DOMAIN:
        thread = threading.Thread(target=make_new_couchdb, args=DOCKER_DOMAIN[instance])
        threads.append(thread)

    for thread in threads:
        thread.setDaemon(True)
        thread.start()

    for thread in threads:
        thread.join()

    register_couchdb_node(DOCKER_DOMAIN['instance1'], DOCKER_DOMAIN['instance2'])
    register_couchdb_node(DOCKER_DOMAIN['instance1'], DOCKER_DOMAIN['instance3'])
    finish_couchdb_cluster(DOCKER_DOMAIN['instance1'])
