from Systems.system import System
import logging
import time
import random

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
        logging.info(f"{node.event.cooldown}/{node.event.cooldown_time}")
        if node.event.cooldown - dt > 0:
            node.event.cooldown -= dt
            self.last_update = now
            return

        node.event.cooldown = node.event.cooldown_time
        node.event.cooldown *= random.random() if node.event.random_cooldown else 1
        node.event.script(node, node.event_active.triggerer)
        self.last_update = now
