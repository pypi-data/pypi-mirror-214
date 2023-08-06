import os

from .couch_config import CouchConfig


class CouchTagDb(object):
    def __init__(self):
        self.couch_config = CouchConfig()
        self.couch_server = self.couch_config.get_couch_server()

    def get_files_with_tag(self, tag):
        for i in self.couch_server.simple_find(
                self.couch_config.get_main_db(),
                {'tags': {
                    "$in": [
                        tag
                    ]
                }}):
            print(f"tagged: {i}")
            path = i['path']
            if os.path.isdir(path):
                for current_dir, _, files in os.walk(path):
                    # Skip subdirs since we're only interested in files.
                    print("====================")
                    print("现在的目录：" + current_dir)
                    print("该目录下包含的子目录：" + str(_))
                    print("该目录下包含的文件：" + str(files))
                    if not _ and not files:
                        print(f"empty: {current_dir}, {_} {files}delete it")
                        os.rmdir(current_dir)
                    for filename in files:
                        relative_path = os.path.join(current_dir, filename)
                        absolute_path = os.path.abspath(relative_path)
                        print("returning: ", absolute_path)
                        yield absolute_path
            else:
                if os.path.exists(path):
                    yield path


if __name__ == "__main__":
    couch_tag_db = CouchTagDb()
    # for i in couch_tag_db.couch_server.simple_find(couch_tag_db.couch_config.get_main_db(),
    #                               {'removed': True}):
    #     print(i)
    for d in couch_tag_db.get_files_with_tag('enc'):
        print(d)
