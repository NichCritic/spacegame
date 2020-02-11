from Systems.system import System
from collections import defaultdict
import math
import logging
import time


class SpatialSystem(System):

    mandatory = ["position"]
    optional = ["area"]
    handles = []

    def __init__(self, node_factory, spatial_map, sector_component):
        self.node_factory = node_factory
        self.spatial_map = spatial_map
        self.sector_component = sector_component

    def handle(self, node):

        if node.entity_has(self.sector_component):
            return
        # logging.info(f"This happens to {node.id}")
        radius = node.area.radius if node.has("area") else 0

        sectors = self.spatial_map.add(
            node.id, node.position.x, node.position.y, radius)
        if node.id == "1f5ae516-324c-4209-93e0-348c98c22ab8":
            logging.info(f"{node.id} in {sectors}")

        node.add_or_attach_component(self.sector_component, {
                                     "sector_rect": sectors})


class SpatialSystemMoved(System):
    mandatory = ["position", "moved"]
    optional = ["area"]
    handles = []

    def __init__(self, node_factory, spatial_map, sector_component):
        self.node_factory = node_factory
        self.spatial_map = spatial_map
        self.sector_component = sector_component
        self.mandatory.append(sector_component)

    def handle(self, node):
        radius = node.area.radius if node.has("area") else 0
        coords = self.spatial_map.move(
            node.id, node.position.x, node.position.y, radius)
        node.add_or_update_component(self.sector_component, {
                                     "sector_rect": coords})
