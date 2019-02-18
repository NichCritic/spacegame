import time
import logging


class System(object):
    manditory = []
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def process(self):
        nodes = self.get_nodes()
        for node in nodes:
            self.handle(node)
            self.clean(node)

    def handle(self, node):
        pass

    def clean(self, node):
        [node.remove_component(c) for c in self.handles]

    def get_nodes(self):
        return self.node_factory.create_node_list(self.manditory,
                                                  self.optional)


class TimedSystem(System):

    def is_timed_out(self, lt, ct, timeout):
        if lt is None:
            return False
        return ct - lt > timeout

    def process(self):
        t = time.time()
        for node in self.get_nodes():
            self.handle(node, t)
            self.clean(node)
