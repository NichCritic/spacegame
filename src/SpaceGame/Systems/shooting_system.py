from Systems.system import System
import math
import time


class ShootingSystem(System):

    manditory = ["shooting", "position",
                 "velocity", "rotation", "physics_update"]
    handles = ["shooting"]

    def handle(self, node):

        x_vel = math.sin(node.rotation.rotation) * 0.1 + node.velocity.x
        y_vel = -math.cos(node.rotation.rotation) * 0.1 + node.velocity.y

        dt = node.physics_update.last_update - node.shooting.time
        if dt < 0:
            dt = 0

        x_pos = node.position.x + math.sin(node.rotation.rotation) * 15
        y_pos = node.position.y - math.cos(node.rotation.rotation) * 15

        now = time.time() * 1000

        self.node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel, 'y': y_vel},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation},
            'area': {'radius': 6},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': now},
            'state_history': {},
            'expires': {
                'expiry_time_ms': 2000,
                'creation_time': now
            },
            # "collidable": {},
            "collision_damage": {"damage": 10},
            "client_sync": {"sync_key": node.shooting.time}
        })
