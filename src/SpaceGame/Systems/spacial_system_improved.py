from Systems.system import System
from collections import defaultdict
import math
import logging
import time


class SpatialSystem(System):

    mandatory = ["position"]
    optional = ["area", "sectors"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sectors = None

    def process(self):
        nodes = self.get_nodes()

        if not self.sectors:
            self.sectors = self.create_sector_dict(nodes, 2500)
            self.fine_sectors = self.create_sector_dict(nodes, 750)

        for node in nodes:
            needs_update = False
            sx, sy = self.get_sector(node, 2500)
            fx, fy = self.get_sector(node, 750)
            if node.has("sector"):

                if node.id not in self.sectors[(sx, sy)]:
                    if node.id in self.sectors[(node.sector.sx, node.sector.sy)]:
                        self.sectors[
                            (node.sector.sx, node.sector.sy)].remove(node.id)
                    self.sectors[(sx, sy)].append(node.id)
                    node.add_or_attach_component("ping_neighbours", {})

                if node.id not in self.fine_sectors[(fx, fy)]:
                    if node.id in self.fine_sectors[(node.sector.fx, node.sector.fy)]:
                        self.fine_sectors[
                            (node.sector.fx, node.sector.fy)].remove(node.id)
                    self.fine_sectors[(fx, fy)].append(node.id)

        node_ids = set([node.id for node in nodes])
        for node in nodes:
            sx, sy, neighbour_entities = self.create_neighbours_list(
                node, self.sectors, 2500)
            fx, fy, fine_neighbour_entities = self.create_neighbours_list(
                node, self.fine_sectors, 750)

            node.add_or_update_component(
                "sector", {"sx": sx, "sy": sy, "neighbours": neighbour_entities,
                           "fx": fx, "fy": fy, "fine_neighbours": fine_neighbour_entities})


'''
0---------------------------2500
|
|
|
|
|
|
|-------------1250------------|
|               |
|               |
|               |
|               |
|               |
2500------------------------2500

'''
