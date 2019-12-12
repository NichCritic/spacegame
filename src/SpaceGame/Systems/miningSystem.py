from Systems.system import System
import math
import logging
import time
import random


class MiningSystem(System):

    mandatory = ["mining", "proximity", "position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        logging.info(f"{node.id} has mining: {node.has('mining')}")

        now = time.time() * 1000
        nnodes = self.node_factory.create_node_list(
            ["position", "area", "minable"], entity_ids=node.proximity.proximity_map.keys())

        if len(nnodes) == 0:
            logging.info("Nothing found to mine")
            return

        closest = min(nnodes, key=lambda n: node.proximity.proximity_map[n.id])

        dist = node.proximity.proximity_map[closest.id]

        if dist > 250:
            return

        v_x = node.position.x - closest.position.x
        v_y = node.position.y - closest.position.y

        n_x = v_x / dist
        n_y = v_y / dist

        t_x = -n_y
        t_y = n_x

        start_x = closest.position.x + n_x * closest.area.radius
        start_y = closest.position.y + n_y * closest.area.radius

        vel_mag = random.randint(1, 100) / 300
        t_vel_mag = random.randint(-20, 20) / 300
        vel_x = n_x * vel_mag + t_x * t_vel_mag
        vel_y = n_y * vel_mag + t_y * t_vel_mag

        if now - node.mining.time > 5000:
            product = random.choice(closest.minable.products)
            self.node_factory.create_new_node({
                'force': {},
                'acceleration': {},
                'velocity': {'x': vel_x / 2, 'y': vel_y / 2},
                'position': {'x': start_x, 'y': start_y},
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
            node.mining.time = now
