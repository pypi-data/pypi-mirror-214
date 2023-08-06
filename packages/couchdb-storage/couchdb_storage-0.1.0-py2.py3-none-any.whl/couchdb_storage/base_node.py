from .net_utils import get_hostname


class BaseNode(object):
    def get_hostname(self):
        return get_hostname()
