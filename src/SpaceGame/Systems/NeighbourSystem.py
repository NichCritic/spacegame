from Systems.system import System
import math
import logging
import time


class CoarseNeighbourSystem(System):

    mandatory = ["course_sectors"]
    optional = []
    handles = []

    def __init__(self, node_factory, spatial_map):
        self.node_factory = node_factory
        self.spatial_map = spatial_map

    def handle(self, node):
        left, right, top, bottom = node.coarse_sectors.sector_rect

        neighbours = self.spatial_map.neighbours_by_sector(
            (left - 1, right + 1, top - 1, bottom + 1))
        node.add_or_attach_component(
            "coarse_neighbours", {"neighbours": neighbours})


class FineNeighbourSystem(System):

    mandatory = ["fine_sectors"]
    optional = []
    handles = []

    def __init__(self, node_factory, spatial_map):
        self.node_factory = node_factory
        self.spatial_map = spatial_map

    def handle(self, node):
        neighbours = self.spatial_map.neighbours_by_sector(
            node.fine_sectors.sector_rect)
        node.add_or_attach_component(
            "fine_neighbours", {"neighbours": neighbours})
