# -*- coding: utf-8 -*-

import docker


class DockerManager(object):
    container = []

    def __init__(self, domain, port):
        url = 'tcp://{}:{}'.format(domain, port)
        self.domain = domain
        self.port = port
        print('[INFO] Connecting Docker %s:%s', domain, port)
        self.client = docker.DockerClient(base_url=url)
        print('[INFO] Connect Docker %s:%s Success! Docker Version: %s' % (domain, port, self.client.version()['Version']))

    def remove_all_container(self):
        for container in self.client.containers.list(all=True):
            print('[INFO] Container %s on %s:%s removed success' % (container.name, self.domain, self.port))
            container.remove(force=True)

    def remove_container(self, name):
        container = self.client.containers.get(name)
        container.remove(force=True)

    def run(self, image=None, name=None, ports=None, detach=None, environment=None, volumes=None):
        print('[INFO] Creating Container %s / %s on %s:%s' % (name, image, self.domain, self.port))

        container = self.client.containers.run(image=image, detach=detach, ports=ports, name=name,
                                               environment=environment, volumes=volumes)
        self.container.append(container)
        print('[INFO] Container %s / %s on %s:%s created success' % (container.name, container.image, self.domain, self.port))

    def list(self):
        containers = self.client.containers.list(all=True)
        print('[INFO] Containers on %s:%s:' % (self.domain, self.port), end='')
        for container in containers:
            print('[%s]: %s ' % (container.name, container.image), end='')
        print()


dockerManager = dict()











