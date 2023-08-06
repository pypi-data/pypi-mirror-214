import os
import pyminizip
import datetime
import time
from couch_storage.couch_tag_db import CouchTagDb


class DuplicatedFileException(Exception):
    pass


# use 1personal so the folder will be on top
target_base_dir = "/storage/emulated/0/1personal"


def handle_enc_tag():
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    target_filename = now_date + '-' + str(int(time.time())) + '.zip'
    couch_tag_db = CouchTagDb()
    file_folders = []
    file_full_path_list = []
    target_folder = os.path.join(target_base_dir, "enc")
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for file in couch_tag_db.get_files_with_tag('enc'):
        if file in file_full_path_list:
            raise DuplicatedFileException
        if '.zip' in file:
            print('ignoring: ', file)
            continue
        if target_folder is None:
            target_folder = os.path.dirname(file)
        file_folders.append(os.path.dirname(file))
        file_full_path_list.append(file)
    compress_level = 0
    print(file_full_path_list, file_folders)
    if len(file_folders) > 0:
        pyminizip.compress_multiple(
            file_full_path_list, file_folders, os.path.join(target_folder, target_filename), '43420024420',
            compress_level
        )
        for file_full_path in file_full_path_list:
            try:
                os.remove(file_full_path)
            except OSError:
                os.rename(file_full_path, file_full_path+".compressed")
                os.remove(file_full_path, file_full_path+".compressed")


if __name__ == '__main__':
    handle_enc_tag()
