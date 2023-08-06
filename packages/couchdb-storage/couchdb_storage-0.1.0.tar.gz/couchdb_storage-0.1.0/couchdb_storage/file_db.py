import os
import time

from .couch_config import CouchConfig
from .taggable import Taggable


class FileDb(object):
    PATH_ATTR_NAME = 'path'
    HOSTNAME_ATTR_NAME = 'hostname'

    def __init__(self):
        c = CouchConfig()
        self.db = c.get_main_db()
        self.server = c.get_couch_server()
        self.hostname = c.get_device_name()

    def get_file_obj_for_path(self, path):
        # How to handle multiple object found for one path?
        data = self.get_basic_taggable_obj_data(path)
        r = self.server.simple_find(self.db, data)
        is_exist = False
        for i in r:
            data = i
            if is_exist:
                print(f"multiple object found: {i} for {path}")
            is_exist = True
        if "size" not in data:
            data["size"] = os.stat(path).st_size
        if "created" not in data:
            data["size"] = time.ctime(os.path.getmtime(path))
        return Taggable(data, self.db)

    def get_basic_taggable_obj_data(self, path):
        data = {
            self.PATH_ATTR_NAME: path,
            self.HOSTNAME_ATTR_NAME: self.hostname,
        }
        return data
