from Systems.system import System
import math
import time
from itertools import takewhile
import logging


class PhysicsSystem(System):

    manditory = ["position", "velocity",
                 "mass", "acceleration", "force", "rotation", "physics_update"]
    optional = ["inventory_mass"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def physics(self, node, packet, pos, vel, mass):
        dt = packet.dt
        node.force.x = packet.force.x + \
            (-vel.x) * 0.03 * dt * (0 if packet.force.x == 0 else 1)
        node.force.y = packet.force.y + \
            (-vel.y) * 0.03 * dt * (0 if packet.force.y == 0 else 1)
        node.rotation.rotation = packet.rotation

        node.acceleration.x = node.force.x / mass
        node.acceleration.y = node.force.y / mass

        node.velocity.x = vel.x + node.acceleration.x * dt
        node.velocity.y = vel.y + node.acceleration.y * dt

        if not packet.brake:
            node.velocity.x = node.velocity.x * (0.99 ** dt)
            node.velocity.y = node.velocity.y * (0.99 ** dt)

        node.position.x = pos.x + node.velocity.x * dt
        node.position.y = pos.y + node.velocity.y * dt

    def handle(self, node):
        physics_packets = node.physics_update.packets

        for packet in physics_packets:
            pos = node.position
            vel = node.velocity

            if node.has("inventory_mass"):
                mass = node.mass.mass + node.inventory_mass.inventory_mass
            else:
                mass = node.mass.mass

            self.physics(node, packet, pos, vel, mass)

            node.physics_update.last_update = packet.time

        node.physics_update.packets = []
