from Systems.system import System
import math


class ShootingSystem(System):

    manditory = ["shooting", "position",
                 "velocity", "rotation", "physics_update"]
    handles = ["shooting"]

    def handle(self, node):

        x_vel = math.sin(node.rotation.rotation) + node.velocity.x
        y_vel = -math.cos(node.rotation.rotation) + node.velocity.y

        dt = node.physics_update.last_update - node.shooting.time
        if dt < 0:
            dt = 0

        x_pos = node.position.x + x_vel * dt
        y_pos = node.position.y + y_vel * dt

        self.node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel, 'y': y_vel},
            'position': {'x': x_pos, 'y': y_pos},
            'rotation': {'rotation': node.rotation.rotation},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {'last_update': node.physics_update.last_update},
            'state_history': {}
        })
