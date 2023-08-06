from couchdb_storage.couch_tag_db import CouchTagDb


class DuplicatedFileException(Exception):
    pass


# use 1personal so the folder will be on top
target_base_dir = "/storage/emulated/0/1personal"


def handle_enc_tag():
    couch_tag_db = CouchTagDb()
    for file in couch_tag_db.get_files_with_tag('enc'):
        print(file)


if __name__ == '__main__':
    handle_enc_tag()
