from Systems.system import System
import math
import logging
import time


class CollisionSystem(System):

    manditory = ["position", "sector", "area", "collidable"]
    optional = ["force"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def handle(self, node):
        nnodes = self.node_factory.create_node_list(
            ["position", "area"], ["force"], entity_ids=node.sector.neighbours)

        for nnode in nnodes:
            if node.id == nnode.id:
                return
            dist = self.distance(node.position, nnode.position)

            if dist == 0:
                dist = 0.01

            comb_radius = node.area.radius + nnode.area.radius
            if dist < comb_radius:
                node.add_or_attach_component("colliding", {'collisions': []})

                node.colliding.collisions.append({
                    "collider": nnode.id,
                    "dist": dist,
                    "delta": comb_radius - dist
                })

                logging.info(f"{node.id} is colliding with {nnode.id}")
