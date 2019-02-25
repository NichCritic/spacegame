from Systems.system import System
import math
import logging
import time


class CollisionSystem(System):

    manditory = ["proximity", "area", "collidable"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        nnodes = self.node_factory.create_node_list(
            ["area", "collidable"], entity_ids=node.proximity.proximity_map.keys())

        for nnode in nnodes:
            if node.id == nnode.id:
                return
            dist = node.proximity.proximity_map[nnode.id]

            comb_radius = node.area.radius + nnode.area.radius
            if dist < comb_radius:
                node.add_or_attach_component("colliding", {'collisions': []})

                node.colliding.collisions.append({
                    "collider": nnode.id,
                    "dist": dist,
                    "delta": comb_radius - dist
                })

                logging.info(f"{node.id} is colliding with {nnode.id}")
