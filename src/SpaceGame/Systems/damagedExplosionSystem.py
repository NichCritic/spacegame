from Systems.system import System
import math
import logging
import time
import random

class DamagedExplosionSystem(System):

    mandatory = ["damaged", "area", "position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        now = time.time() * 1000
        rotation = random.random()*2*math.pi
        magnitude = random.random()*node.area.radius

        x = node.position.x + math.sin(rotation) * magnitude
        y = node.position.y - math.cos(rotation) * magnitude

        self.node_factory.create_new_node({
            "position": {"x":x, "y": y},
            "area": {"radius":5},
            'type': {'type': 'explosion'},
            "expires": {
                'expiry_time_ms': 1000,
                'creation_time': now
            },
            'animated': {'update_rate': 200},
            'updated': {}
        })