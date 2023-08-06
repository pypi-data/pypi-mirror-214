from couchdb_storage.node_factory import NodeFactory
import unittest


class TestStringMethods(unittest.TestCase):
    def test_node_factory(self):
        node = NodeFactory.get_node()
        print(f"hostname is: {node.get_hostname()}")
        print(f"clipboard files are: {node.get_clipboard_file_list()}")


if __name__ == '__main__':
    unittest.main()
