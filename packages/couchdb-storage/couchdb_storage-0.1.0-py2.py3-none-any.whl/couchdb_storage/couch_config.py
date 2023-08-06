import json
from pathlib import Path
import uuid
import time
import jsoncfg
from .couch_db_storage import CouchDbStorage
# Combine simple-config and jsoncfg. Use simple-config to manage file and update jsoncfg by generating json string


class CouchConfig(object):
    CONFIG_FILE_NAME = "couch_config.json"

    def __init__(self, config_folder=None):
        self.couch_server = None
        self.db = None
        self.config_full_path = config_folder
        if self.config_full_path is None:
            self.config_full_path = Path(Path(__file__).parents[1], self.CONFIG_FILE_NAME)
        if not self.config_full_path.exists():
            password = input('please input password: ')
            default_config = {
                    "uuid": str(uuid.uuid4()),
                    "couch_server": "www.weijia.asia",
                    "couch_user": "agr",
                    "main_db": "agr",
                    "device_name": "",
                    "couch_password": password,
            }
            with open(self.config_full_path, "w") as f:
                json.dump(default_config, f)
        self.config = jsoncfg.load_config(str(self.config_full_path))

        self.couch_server = CouchDbStorage(self.config.couch_server(),
                                           self.config.couch_user(),
                                           self.config.couch_password())

    def get_config(self, config_name, default_value=None):
        basic_dict = {"device_uuid": self.config.uuid(), "name": config_name, "type": "configs"}
        return self.get_config_with_base(basic_dict, config_name, default_value)

    def get_config_with_base(self, basic_dict, config_name, default_value):
        basic_dict["name"] = config_name
        self.db = self.get_main_db()
        r = self.couch_server.simple_find(self.db, basic_dict)
        for i in r:
            return i["value"]
        basic_dict["value"] = default_value
        timestamp = time.time()
        basic_dict["created"] = timestamp
        basic_dict["last_updated"] = timestamp
        self.db.save(basic_dict)
        return default_value

    def get_global_config(self, config_name, default_value=None):
        basic_dict = {"name": config_name, "type": "configs"}
        return self.get_config_with_base(basic_dict, config_name, default_value)

    def get_main_db(self):
        if self.db is None:
            main_db = self.config.main_db()
            self.db = self.couch_server.get_db(main_db)
        return self.db

    def get_couch_server(self):
        return self.couch_server

    def get_device_uuid(self):
        return self.config.uuid()

    def get_db(self, db_name):
        return self.couch_server.get_db(db_name)

    def get_device_name(self):
        return self.config.device_name()


if __name__ == "__main__":
    c = CouchConfig()
    print(c.get_device_uuid())
    print(c.get_config("test_config", "test_value"))
    print(c.get_config("test_config", "test_value_2"))
