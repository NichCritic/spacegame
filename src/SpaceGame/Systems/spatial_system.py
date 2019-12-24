from Systems.system import System
from collections import defaultdict
import math
import logging
import time

class SpatialSystem(System):

    mandatory = ["position"]
    optional = ["sector"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sectors = None
        self.fine_sectors = None

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

    def get_sector(self, node, sector_size):
        sx = math.floor(node.position.x / sector_size)
        sy = math.floor(node.position.y / sector_size)
        return sx, sy

    def process(self):
        nodes = self.get_nodes()

        if not self.sectors:
            self.sectors = self.create_sector_dict(nodes, 2500)
            self.fine_sectors = self.create_sector_dict(nodes, 250)


        for node in nodes:
            needs_update = False
            sx, sy = self.get_sector(node, 2500)
            fx, fy = self.get_sector(node, 250)
            if node.has("sector"):
                
                if node.id not in self.sectors[(sx, sy)]:
                    if node.id in self.sectors[(node.sector.sx, node.sector.sy)]:
                        self.sectors[(node.sector.sx, node.sector.sy)].remove(node.id)
                    self.sectors[(sx, sy)].append(node.id)
                    node.add_or_attach_component("ping_neighbours", {})
                
                if node.id not in self.fine_sectors[(fx, fy)]:
                    if node.id in self.fine_sectors[(node.sector.fx, node.sector.fy)]:
                        self.fine_sectors[(node.sector.fx, node.sector.fy)].remove(node.id)
                    self.fine_sectors[(fx, fy)].append(node.id)
            
            
        
        node_ids = set([node.id for node in nodes])
        for node in nodes:
            sx, sy, neighbour_entities = self.create_neighbours_list(
                node, self.sectors, 2500)
            fx, fy, fine_neighbour_entities = self.create_neighbours_list(
                node, self.fine_sectors, 250)
             
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
