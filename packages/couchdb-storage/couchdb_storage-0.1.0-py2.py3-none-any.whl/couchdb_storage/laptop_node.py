import os
import subprocess
import json


class TermuxNode(object):
    def get_battery_status(self):
        return {"battery": "100%"}

