from couchdb_storage.termux_node import TermuxNode
from couchdb_storage.windows_node import WindowsNode


class NodeFactory(object):
    @staticmethod
    def get_node():
        try:
            node = TermuxNode()
            node.get_battery_status()
            return node
        except FileNotFoundError:
            return WindowsNode()


if __name__ == "__main__":
    NodeFactory.get_node()
