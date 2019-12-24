from Systems.system import System
import math
import logging
import time


class AttachDeathSystem(System):

    mandatory = ["attached"]
    optional = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        parent_node = self.node_factory.create_node(
            node.attached.target_id, [], ['dead'])

        if parent_node.has("dead"):
            node.add_or_attach_component("dead", {})
