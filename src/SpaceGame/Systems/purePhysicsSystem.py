from Systems.system import System
import math
import time
from itertools import takewhile


class PhysicsSystem(System):

    manditory = ["position", "velocity",
                 "mass", "acceleration", "force", "rotation", "physics_update"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def physics(self, node, packet, pos, vel, mass):
        node.force.x = packet.force.x
        node.force.y = packet.force.y
        node.rotation.rotation = packet.rotation
        dt = packet.dt

        # print(f"{node.force.y}, {dt}")

        node.acceleration.x = node.force.x / mass
        node.acceleration.y = node.force.y / mass

        # print(f'{node.acceleration.x}, {node.acceleration.y}')

        node.velocity.x = vel.x + node.acceleration.x * dt
        node.velocity.y = vel.y + node.acceleration.y * dt

        if not packet.brake:
            node.velocity.x = node.velocity.x * (0.99 ** dt)
            node.velocity.y = node.velocity.y * (0.99 ** dt)

        # print(f'{node.velocity.x}, {node.velocity.y}')

        node.position.x = pos.x + node.velocity.x * dt
        node.position.y = pos.y + node.velocity.y * dt

    def handle(self, node):

        physics_packets = node.physics_update.packets

        # print(list(inputlist))

        for packet in physics_packets:
            pos = node.position
            vel = node.velocity
            mass = node.mass.mass

            self.physics(node, packet, pos, vel, mass)

            node.physics_update.last_update = packet.time

        node.physics_update.packets = []
