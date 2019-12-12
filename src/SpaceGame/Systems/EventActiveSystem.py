from Systems.system import System
import logging
import time


class EventActiveSystem(System):

    mandatory = ["event", "event_active"]
    optional = []
    handles = ["event_active"]

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.last_update = time.time() * 1000

    def handle(self, node):
        now = time.time() * 1000
        dt = now - self.last_update
        if node.event.cooldown - dt > 0:
            node.event.cooldown -= dt
            return

        node.event.cooldown = node.event.cooldown_time
        node.event.script(node)
        self.last_update = now
