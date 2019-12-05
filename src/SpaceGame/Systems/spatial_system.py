from Systems.system import System
from collections import defaultdict
import math
import logging

class SpatialSystem(System):

    manditory = ["position"]
    optional = ["sector"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def create_sector_dict(self, nodes, sector_size):
        sectors = defaultdict(list)

        for node in nodes:
            sx = math.floor(node.position.x / sector_size)
            sy = math.floor(node.position.y / sector_size)
            sectors[(sx, sy)].append(node.id)

        return sectors

    def create_neighbours_list(self, node, sectors, sector_size):
        sx = math.floor(node.position.x / sector_size)
        sy = math.floor(node.position.y / sector_size)

        half = sector_size / 2

        top = True if node.position.y < sy * sector_size + half else False
        left = True if node.position.x < sx * sector_size + half else False

        if top and left:
            neighbors = [(-1, -1), (0, -1), (-1, 0), (0, 0)]
        if top and not left:
            neighbors = [(0, -1), (1, -1), (1, 0), (0, 0)]
        if not top and left:
            neighbors = [(-1, 0), (-1, 1), (0, 1), (0, 0)]
        if not top and not left:
            neighbors = [(1, 0), (1, 1), (0, 1), (0, 0)]

        neighbor_entities = sum([sectors[(sx + n[0], sy + n[1])]
                                 for n in neighbors], [])
        return sx, sy, neighbor_entities

    def process(self):
        nodes = self.get_nodes()

        sectors = self.create_sector_dict(nodes, 2500)
        fine_sectors = self.create_sector_dict(nodes, 750)



        for node in nodes:
            neighbours_cache = []
            if node.has("sector"):
                neighbours_cache = node.sector.neighbours

            sx, sy, neighbour_entities = self.create_neighbours_list(
                node, sectors, 2500)
            fx, fy, fine_neighbour_entities = self.create_neighbours_list(
                node, fine_sectors, 750)

            # logging.info(neighbours_cache)
            # logging.info(neighbour_entities)
            [self.node_factory.create_node(e, {}).add_or_attach_component("updated", {}) for e in neighbour_entities if e not in neighbours_cache]
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
