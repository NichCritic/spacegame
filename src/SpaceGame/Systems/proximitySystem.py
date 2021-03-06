from Systems.system import System
import math
import logging
import time


class ProximitySystem(System):

    manditory = ["position", "sector", "velocity", "moved"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def handle(self, node):
        # lgging.info(node.sector.fine_neighbours)
        nnodes = self.node_factory.create_node_list(
            ["position", "area"], [], entity_ids=node.sector.fine_neighbours)

        node.add_or_attach_component("proximity", {})
        node.proximity.proximity_map = {}

        for nnode in nnodes:
            if node.id == nnode.id:
                continue
            dist = self.distance(node.position, nnode.position)

            if dist == 0:
                dist = 0.01

            node.proximity.proximity_map[nnode.id] = dist
            nnode.add_or_attach_component("proximity", {})
            nnode.proximity.proximity_map[node.id] = dist
