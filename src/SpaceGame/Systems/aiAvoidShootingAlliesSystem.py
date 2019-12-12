from Systems.system import System
import math
import time
import logging


class AIAvoidShootingAlliesSystem(System):

    mandatory = ["avoid_shooting_allies", "allies", "proximity", "rotation", "position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def get_allies(self, keys):
        # logging.info(keys)
        nodes = self.node_factory.create_node_list(["allies"], [], entity_ids = keys)
        return nodes

    def handle(self, node):

        allies = self.get_allies(node.proximity.proximity_map.keys())

        for ally in allies:
            if node.id == ally.id:
                continue

            if node.allies.team != ally.allies.team:
                continue

            t_node = self.node_factory.create_node(
                ally.id, [], ["position"])

            # Target was removed before this system was run
            if not t_node.has("position"):
                return

            y2 = t_node.position.y
            y = node.position.y
            x2 = t_node.position.x
            x = node.position.x

            angle = math.atan2((y2 - y), (x2 - x)) + math.pi / 2

            current_angle = node.rotation.rotation

            five_degrees_rad = 0.0872665

            shoot = angle < current_angle + five_degrees_rad and angle > current_angle - five_degrees_rad

            node.add_or_attach_component("impulses", {})

            node.impulses.shoot -= 10 if shoot else 0  
