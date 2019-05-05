# -*- coding: utf-8 -*-

from swiftclient import client
from swiftclient.exceptions import ClientException
from io import BytesIO
import logging

from backend.config.config import *


logger = logging.getLogger('django.debug')


class ObjectStorageHandler(object):
    swift = None
    container_name = None
    container_url = None

    def __init__(self, container_name, object_storage_url=OBJECT_STORAGE_URL, authurl=OS_AUTH_URL, user=OS_USERNAME,
                 key=OS_PASSWORD, tenant_name=OS_TENANT_ID, auth_version=OS_VERSION):
        self.swift = client.Connection(authurl=authurl, preauthurl=OBJECT_STORAGE_PREURL, user=user, key=key,
                                       tenant_name=tenant_name, auth_version=auth_version, retries=3, timeout=5,
                                       force_auth_retry=True)
        self.container_name = container_name
        self.container_url = '{}/{}/'.format(object_storage_url, container_name)
        self.check_exist_or_create()
        logger.debug('Object Storage Connected Success: %s' % self.container_url)

    def reconnect(self):
        del self.swift
        self.__init__(self.container_name)

    def check_exist_or_create(self):
        try:
            self.swift.get_container(self.container_name)
        except ClientException:
            self.swift.put_container(self.container_name)

    def findall(self):
        return self.swift.get_container(self.container_name)[1]

    def find(self, name=None):
        items = self.findall()
        if not name:
            return items
        return [item for item in items if name in item['name']]

    def upload(self, file_name, file):
        return self.swift.put_object(container=self.container_name, obj=file_name, contents=file)

    def delete(self, file_name):
        return self.swift.delete_object(container=self.container_name, obj=file_name)

    def download(self, file_name):
        try:
            resp = list(self.swift.get_object(container=self.container_name, obj=file_name))
        except ClientException:
            logger.error('Object Storage File [%s] Not Found', file_name)
            return None

        file = BytesIO(resp[-1])
        return file

    def remove_all(self):
        for pic in self.findall():
            print('OS DELETE: %s' % pic['name'])
            try:
                self.delete(pic['name'])
            except Exception as e:
                print(e)
                continue
        logger.debug('All Files in Object Storage Removed')

    def delete_container(self):
        return self.swift.delete_container(container=self.container_name)


object_storage_handler = ObjectStorageHandler(OBJECT_STORAGE_CONTAINER)


if __name__ == '__main__':
    # object_storage_handler.remove_all()
    pass


