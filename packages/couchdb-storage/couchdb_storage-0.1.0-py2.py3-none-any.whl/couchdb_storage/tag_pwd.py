import os
from .tag_utils import interact_with_user_for_tagging_path


def main():
    current_folder = os.getcwd() + os.sep
    tag_path(current_folder)


def tag_path(path):
    interact_with_user_for_tagging_path(path)


if __name__ == "__main__":
    main()
