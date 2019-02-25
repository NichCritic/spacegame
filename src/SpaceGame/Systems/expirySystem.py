from Systems.system import System
import time


class ExpirySystem(System):

    manditory = ["expires"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        now = time.time()
        creation_time = node.expires.creation_time
        expiry_time = node.expires.expiry_time_ms
        if(now * 1000 - creation_time > expiry_time):
            node.remove_all_components()
