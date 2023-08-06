from couch_storage.file_db import FileDb
from couch_storage.tag_utils import interact_with_user_for_tagging_path
from node_factory import NodeFactory
from tag_pwd import tag_path


def main():
    node = NodeFactory.get_node()
    file_list = node.get_clipboard_file_list()
    last_tag_str = ""
    for file in file_list:
        last_tag_str = interact_with_user_for_tagging_path(file, last_tag_str)


if __name__ == "__main__":
    main()
