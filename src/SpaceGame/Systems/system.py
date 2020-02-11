import time
import logging


class System(object):
    mandatory = []
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def process(self):
        nodes = self.get_nodes()
        # start = time.time()
        for node in nodes:
            self.handle(node)
            self.clean(node)
        # end = time.time()
        # dt = end - start
        # logging.info(f"{self.__class__.__name__} processed {len(nodes)}
        # nodes")

    def handle(self, node):
        pass

    def clean(self, node):
        [node.remove_component(c) for c in self.handles]

    def get_nodes(self):

        nodes = self.node_factory.create_node_list(self.mandatory,
                                                   self.optional)
        # for n in nodes:
        #     for c in self.mandatory:
        #         if not n.has(c):
        #             logging.error(f"PANIC: {n.id} does not have mandatory component {c} requested by {self.__class__.__name__}")
        #             import pdb
        #             pdb.set_trace()
        #             nodes = self.node_factory.create_node_list(self.mandatory,
        #                                                        self.optional)

        return nodes


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
