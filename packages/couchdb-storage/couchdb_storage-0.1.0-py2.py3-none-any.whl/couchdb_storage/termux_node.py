import os
import subprocess
import json

from .base_node import BaseNode


def parse_total_cmd_clipboard_file_list(total_cmd_clipboard_data):
    lines = total_cmd_clipboard_data.split('\n')
    folder = None
    header_lines_to_read = 2
    files = []
    for line in lines:
        if line.replace("\r", "") == "":
            continue
        if header_lines_to_read > 0:
            header_lines_to_read -= 1
            print("skipping: ", line)
            continue
        if folder is None:
            folder = line
            print("folder is: ", folder)
            continue
        files.append(os.path.join(folder, line.split('\t')[0]))
    return files


def get_termux_node_name():
    lines = subprocess.check_output("getprop").decode()
    #print(lines)
    for line in lines.split("\n"):
        #print(line)
        if "persist.sys.device_name" in line:
            return line.split(":")[1].strip().replace("[", "").replace("]", "")


class TermuxNode(BaseNode):
    def get_battery_status(self):
        return json.loads(subprocess.check_output("termux-battery-status"))

    def get_clipboard_data(self):
        return subprocess.check_output("termux-clipboard-get").decode()

    def get_clipboard_file_list(self):
        return parse_total_cmd_clipboard_file_list(self.get_clipboard_data())

    def get_hostname(self):
        return get_termux_node_name()


if __name__ == "__main__":
    node = TermuxNode()
    print(node.get_hostname())
    print(node.get_clipboard_file_list())
