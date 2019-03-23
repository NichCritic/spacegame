from Systems.system import System
import math
import time
import logging


class AIOrientTowardsTargetSystem(System):

    manditory = ["orient_towards_target", "target", "rotation", "position"]
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

        alternative_angle = -1 * angle + (-2 if angle < 0 else 2) * math.pi

        direction = "left"

        if current_angle - angle == 0:
            direction = "none"
        elif current_angle - angle > 0:
            direction = "left"
        else:
            direction = "right"
        # else:
            # if current_angle - alternative_angle > 0:
            # direction = "right"  # ???
            # else:
            # direction = "right"  # ???

        node.add_or_attach_component("player_input", {})

        node.player_input.data.extend([{
            "left": True if direction == "left" else False,
            "right": True if direction == "right" else False,
            "dt": 50,
            "time": time.time() * 1000,
            "shoot": False,
            "thrust": True,
            "mining": False,
            "brake": False,
            "was_processed": False
        }])
