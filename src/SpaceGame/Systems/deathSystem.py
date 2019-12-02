from Systems.system import System
import math
import logging
import time


class DeathSystem(System):

    manditory = ["dead"]
    optional = []
    handles = ["dead"]

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        now = time.time() * 1000
        node.add_or_attach_component('position', {})
        pos = node.position
        node.remove_all_components()
        node.add_or_update_component('type', {'type': 'explosion'})
        node.add_or_update_component(
            'position', {'x': pos.x, 'y': pos.y})
        # node.add_or_update_component(
        #     'health', {'health': 0, 'max_health': 0})
        node.add_or_update_component('expires', {
            'expiry_time_ms': 1000,
            'creation_time': now
        })
        node.add_or_attach_component('area', {'radius': 25})
        node.add_or_attach_component(
            'animated', {'update_rate': 200})
        node.add_or_attach_component('updated', {})