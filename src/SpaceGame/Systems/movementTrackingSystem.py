from Systems.system import System
import math
import logging
import time


class MovementTrackingSystem(System):

    manditory = ["position", "velocity"]
    optional = ["moved"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.position_cache = {}

    def handle(self, node):
        if node.id not in self.position_cache:
            self.position_cache[node.id] = {
                'x': node.position.x, 'y': node.position.y}
            node.add_or_attach_component('moved', {})
            node.add_or_attach_component('updated', {})
            return

        if node.position.x != self.position_cache[node.id]['x'] or node.position.y != self.position_cache[node.id]['y']:
            node.add_or_attach_component('moved', {})
            node.add_or_attach_component('updated', {})
            self.position_cache[node.id] = {
                'x': node.position.x, 'y': node.position.y}
        elif node.has("moved"):
            node.remove_component("moved")
