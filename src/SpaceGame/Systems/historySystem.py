from Systems.system import System
import math
import time
from itertools import takewhile


class HistorySystem(System):

    manditory = ["state_history", "position", "velocity",
                 "mass", "acceleration", "force", "rotation", "physics_update"]
    optional = ["inventory_mass"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        state = {
            "position": {"x": node.position.x, "y": node.position.y},
            "velocity": {"x": node.velocity.x, "y": node.velocity.y},
            "acceleration": {"x": node.acceleration.x, "y": node.acceleration.y},
            "force": {"x": node.force.x, "y": node.force.y},
            "mass": node.mass.mass + node.inventory_mass.inventory_mass if node.has("inventory_mass") else 0,
            "rotation": node.rotation.rotation,
            "physics_packets": [p.to_dict() for p in node.physics_update.packets],
            "time": node.physics_update.last_update
        }

        node.state_history.history.append(state)
        if len(node.state_history.history) > 10:
            node.state_history.history.pop(0)
