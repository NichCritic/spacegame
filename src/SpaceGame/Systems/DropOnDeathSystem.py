from Systems.system import System
import math
import logging
import time
import random


class DropOnDeathSystem(System):

    mandatory = ["drop_on_death", "position", "dead"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        now = time.time() * 1000
        for _ in range(node.drop_on_death.qty):
            product = random.choice(node.drop_on_death.products)
            angle = random.random() * math.pi * 2
            mag = random.random() / 32
            vel_x = math.sin(angle) * mag
            vel_y = math.cos(angle) * mag

            self.node_factory.create_new_node({
                'force': {},
                'acceleration': {},
                'velocity': {'x': vel_x, 'y': vel_y},
                'position': {'x': node.position.x, 'y': node.position.y},
                'rotation': {'rotation': 0},
                'mass': {},
                'server_updated': {},
                'type': {'type': f'{product.name.replace(" ", "_")}_pickup'},
                'area': {'radius': 16},
                'physics_update': {},
                'state_history': {},
                'expires': {
                    'expiry_time_ms': 20000,
                    'creation_time': now
                },
                "collidable": {},
                "pickup": {
                    "item_id": product.id,
                    "qty": 1
                }
            })
