from __future__ import print_function

import json
import os


CONFIG_PATH = os.path.join(os.path.abspath(__file__), 'config/config.json')


class Configuration(object):

    def __init__(self, safe=True):
        self.safe = safe
        self.data = {}
        self.loaded = False

    def load(self):
        try:
            with open(CONFIG_PATH, 'r') as cfg:
                self.data = json.load(cfg)
            self.loaded = True
        except (IOError, ValueError) as e:
            print("Could not load config: {}".format(e))
            if not self.safe:
                raise e

    def __getattr__(self, item):
        if not self.loaded:
            self.load()

        if self.safe:
            return self.data.get(item)
        return self.data[item]
