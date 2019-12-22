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

        neighbours_cache = {}

        for node in nodes:
            needs_update = False
            sx, sy = self.get_sector(node, 2500)
            fx, fy = self.get_sector(node, 250)
            if node.has("sector"):
                neighbours_cache[node.id] = set(node.sector.neighbours)
                
                if node.id not in self.sectors[(sx, sy)]:
                    if node.id in self.sectors[(node.sector.sx, node.sector.sy)]:
                        self.sectors[(node.sector.sx, node.sector.sy)].remove(node.id)
                    self.sectors[(sx, sy)].append(node.id)
                
                if node.id not in self.fine_sectors[(fx, fy)]:
                    if node.id in self.fine_sectors[(node.sector.fx, node.sector.fy)]:
                        self.fine_sectors[(node.sector.fx, node.sector.fy)].remove(node.id)
                    self.fine_sectors[(fx, fy)].append(node.id)
            else:
                neighbours_cache[node.id] = set()
            
        dt1=0           
        dt2=0           
        dt3=0           
        dt4=0

        # updated_count = 0
        update_set = set()           
        for node in nodes:
            t1 = time.time()
            sx, sy, neighbour_entities = self.create_neighbours_list(
                node, self.sectors, 2500)
            t2 = time.time()
            fx, fy, fine_neighbour_entities = self.create_neighbours_list(
                node, self.fine_sectors, 250)
            t3 = time.time()
            # updated_count += len(set(neighbour_entities) - neighbours_cache[node.id])
            update_set |= (set(neighbour_entities) - neighbours_cache[node.id])
             
            t4 = time.time()
            node.add_or_update_component(
                "sector", {"sx": sx, "sy": sy, "neighbours": neighbour_entities,
                           "fx": fx, "fy": fy, "fine_neighbours": fine_neighbour_entities})
            t5 = time.time()
            dt1 += t2-t1
            dt2 += t3-t3
            dt3 += t4-t3
            dt4 += t5-t4

        [self.node_factory.create_node(e, {}).add_or_attach_component("updated", {}) for e in update_set]
        logging.info(f"Processing {len(nodes)} nodes")
        # logging.info(f"Update count: {updated_count}")
        logging.info(f"Update set len: {len(update_set)}")

        if len(update_set) > len(nodes):
            print(update_set)
        logging.info(f"Stage 1 is {dt1}s")
        logging.info(f"Stage 2 is {dt2}s")
        logging.info(f"Stage 3 is {dt3}s")
        logging.info(f"Stage 4 is {dt4}s")



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
