from Systems.system import System
import math
import logging
import time


class CoarseNeighbourSystem(System):

    mandatory = ["sectors_coarse"]
    optional = []
    handles = []

    def __init__(self, node_factory, spatial_map):
        self.node_factory = node_factory
        self.spatial_map = spatial_map

    def handle(self, node):
        # logging.info(f"coarse neighbours handles {node.id}")
        left, right, top, bottom = node.sectors_coarse.sector_rect

        neighbours = self.spatial_map.neighbours_by_sector(
            (left - 1, right + 1, top - 1, bottom + 1))

        if node.id == "1f5ae516-324c-4209-93e0-348c98c22ab8":
            logging.info(f"{left, right, top, bottom}, {neighbours}")

        node.add_or_update_component(
            "neighbours_coarse", {"neighbours": neighbours})


class FineNeighbourSystem(System):

    mandatory = ["sectors_fine"]
    optional = []
    handles = []

    def __init__(self, node_factory, spatial_map):
        self.node_factory = node_factory
        self.spatial_map = spatial_map

    def handle(self, node):
        neighbours = self.spatial_map.neighbours_by_sector(
            node.sectors_fine.sector_rect)
        node.add_or_update_component(
            "neighbours_fine", {"neighbours": neighbours})
