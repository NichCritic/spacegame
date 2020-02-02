from Systems.system import System
import math
import logging
import time


class CoarseProximitySystem(System):

    mandatory = ["position", "neighbours_coarse", "moved"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def distance(self, p1, p2):
        return math.abs((p1.x - p2.x)) + math.abs((p1.y - p2.y))

    def handle(self, node):

        nnodes = self.node_factory.create_node_list(
            ["position"], [], entity_ids=node.coarse_neighbours.neighbours)

        node.add_or_attach_component("proximity", {})
        node.proximity.proximity_map = {}

        # logging.info(f"Proximity handling {len(nnodes)} neighbours")

        for nnode in nnodes:
            if node.id == nnode.id:
                continue
            dist = distance(self, p1, p2)

            if dist == 0:
                dist = 0.01

            node.proximity.proximity_map[nnode.id] = dist
            nnode.add_or_attach_component("proximity", {})
            nnode.proximity.proximity_map[node.id] = dist
