from Systems.system import System
import math
import time
import logging


class AIReturnHomeSystem(System):

    manditory = ["ai_return_home", "home", "rotation", "position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        
        y2 = node.home.y
        y = node.position.y
        x2 = node.home.x
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

        node.add_or_attach_component("impulses", {})

        node.impulses.left += 100 if direction == "left" else 0
        node.impulses.right += 100 if direction == "right" else 0
        node.impulses.thrust += 100
