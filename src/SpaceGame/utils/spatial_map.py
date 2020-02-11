import math
from collections import defaultdict
import logging


class SpatialMap():

    def __init__(self, size):
        self.size = size
        self.map = defaultdict(set)
        self.entity_map = defaultdict(set)

    def add(self, id, x, y, radius=0):
        s_left = math.floor((x - radius) / self.size)
        s_right = math.floor((x + radius) / self.size)

        s_top = math.floor((y - radius) / self.size)
        s_bottom = math.floor((y + radius) / self.size)

        for j in range(s_top, s_bottom + 1):
            for i in range(s_left, s_right + 1):
                if id == "1f5ae516-324c-4209-93e0-348c98c22ab8":
                    logging.info(f"{id} added to {i, j}")
                self.map[(i, j)].add(id)
                self.entity_map[id].add((i, j))

        return (s_left, s_right, s_top, s_bottom)

    def move(self, id, x, y, radius):
        s_left = math.floor((x - radius) / self.size)
        s_right = math.floor((x + radius) / self.size)

        s_top = math.floor((y - radius) / self.size)
        s_bottom = math.floor((y + radius) / self.size)

        coords = set([(i, j) for i in range(s_left, s_right + 1)
                      for j in range(s_top, s_bottom + 1)])

        old_coords = self.entity_map[id] - coords
        new_coords = coords - self.entity_map[id]

        self.entity_map[id] = coords
        for coord in old_coords:
            self.map[coord].remove(id)

        for coord in new_coords:
            self.map[coord].add(id)
        return (s_left, s_right, s_top, s_bottom)

    def remove(self, id):
        for coord in self.entity_map[id]:
            self.map[coord].remove(id)
        del self.entity_map[id]

    def neighbours_by_sector(self, sector_rect):
        s_left, s_right, s_top, s_bottom = sector_rect

        coords = set([(i, j) for i in range(s_left, s_right + 1)
                      for j in range(s_top, s_bottom + 1)])
        ns = set()

        # logging.info(f"{self.map[(-6, -3)]}")
        for co in coords:
            # if "1f5ae516-324c-4209-93e0-348c98c22ab8" in self.map[co]:
            ns |= self.map[co]
        return ns

    def neighbours_surround(self, x, y, radius):
        s_left = math.floor((x - radius) / self.size) - 1
        s_right = math.floor((x + radius) / self.size) + 1

        s_top = math.floor((y - radius) / self.size) - 1
        s_bottom = math.floor((y + radius) / self.size) + 1

        coords = set([(i, j) for i in range(s_left, s_right + 1)
                      for j in range(s_top, s_bottom + 1)])
        ns = set()
        for co in coords:
            ns |= self.map[co]
        return ns

    def neighbours(self, id):
        ns = set()
        for coord in self.entity_map[id]:
            ns |= self.map[coord]
        return ns

    def neighbours_coords(self, x, y):
        s_x, s_y = math.floor(x / self.size), math.floor(y / self.size)
        return self.map[(s_x, s_y)]
