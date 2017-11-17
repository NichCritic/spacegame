from Systems.system import System
import math


class ShootingSystem(System):

    manditory = ["shooting", "position", "velocity", "rotation"]
    handles = ["shooting"]

    def handle(self, node):

        x_vel = 0.7 * math.sin(node.rotation.rotation) + node.velocity.x
        y_vel = -0.7 * math.cos(node.rotation.rotation) + node.velocity.y

        self.node_factory.create_new_node({
            'force': {},
            'acceleration': {},
            'velocity': {'x': x_vel, 'y': y_vel},
            'position': {'x': node.position.x, 'y': node.position.y},
            'rotation': {'rotation': node.rotation.rotation},
            'mass': {},
            'server_updated': {},
            'type': {'type': 'bolt'},
            'physics_update': {}
        })
