# -*- coding: utf-8 -*-

from swiftclient import client, exceptions
from PIL import Image
from io import BytesIO

from backend.common.config import *


class ObjectStorageHandler(object):
    swift = None
    container_name = None
    container_url = None

    def __init__(self, container_name, object_storage_url=OBJECT_STORAGE_URL, authurl=OS_AUTH_URL, user=OS_USERNAME,
                 key=OS_PASSWORD, tenant_name=OS_TENANT_ID, auth_version=OS_VERSION):
        self.swift = client.Connection(authurl=authurl, user=user, key=key, tenant_name=tenant_name, auth_version=auth_version)
        self.container_name = container_name
        self.container_url = '{}/{}/'.format(object_storage_url, container_name)
        self.check_exist_or_create()

    def check_exist_or_create(self):
        try:
            self.swift.get_container(self.container_name)
        except exceptions.ClientException:
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
        resp = list(self.swift.get_object(container=self.container_name, obj=file_name))
        params = resp[0]

        file = BytesIO(resp[-1])
        if params['content-type'] == 'image/jpeg':
            image = (Image.open(file)).convert('RGB')
            return image
        return file

    def delete_container(self):
        return self.swift.delete_container(container=self.container_name)


object_storage_handler = ObjectStorageHandler(OBJECT_STORAGE_CONTAINER)


if __name__ == '__main__':
    test_os_handler = ObjectStorageHandler('test_container')
    with open('../common/test_file.jpg', 'rb') as f:
        test_os_handler.upload('test.jpg', f)
    contents = test_os_handler.findall()
    for content in contents:
        print(content)
    image = test_os_handler.download('test.jpg')
    print(image)
    test_os_handler.delete('test.jpg')
    test_os_handler.delete_container()
