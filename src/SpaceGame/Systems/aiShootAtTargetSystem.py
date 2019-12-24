from Systems.system import System
import math
import time
import logging


class AIShootAtTargetSystem(System):

    mandatory = ["shoot_at_target", "target", "rotation", "position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):

        t_node = self.node_factory.create_node(
            node.target.id, [], ["position"])

        # Target was removed before this system was run
        if not t_node.has("position"):
            return

        y2 = t_node.position.y
        y = node.position.y
        x2 = t_node.position.x
        x = node.position.x

        angle = math.atan2((y2 - y), (x2 - x)) + math.pi / 2

        current_angle = node.rotation.rotation

        one_rad = 0.0174533

        firing_angle = node.shoot_at_target.firing_angle * one_rad

        shoot = angle < current_angle + firing_angle and angle > current_angle - firing_angle

        node.add_or_attach_component("impulses", {})

        node.impulses.shoot += 100 if shoot else 0 
