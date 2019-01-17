from Systems.system import System
from collections import defaultdict
import math


class SpatialSystem(System):

    manditory = ["position"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def process(self):
        nodes = self.get_nodes()

        sectors = defaultdict(list)

        for node in nodes:
            sx = math.floor(node.position.x / 2500)
            sy = math.floor(node.position.y / 2500)
            sectors[(sx, sy)].append(node.id)

        for node in nodes:
            sx = math.floor(node.position.x / 2500)
            sy = math.floor(node.position.y / 2500)

            top = True if node.position.y < sy * 2500 + 1250 else False
            left = True if node.position.x < sx * 2500 + 1250 else False

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
            node.add_or_update_component(
                "sector", {"sx": sx, "sy": sy, "neighbours": neighbor_entities})


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
