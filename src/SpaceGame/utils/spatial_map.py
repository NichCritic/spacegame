import math
from collections import defaultdict


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

        for j in range(s_top, s_bottom):
            for i in range(s_left, s_right):
                self.map[(i, j)].add(id)
                self.entity_map[id].add((i, j))

        return self.entity_map[id]

    def move(self, id, x, y, radius):
        s_left = math.floor((x - radius) / self.size)
        s_right = math.floor((x + radius) / self.size)

        s_top = math.floor((y - radius) / self.size)
        s_bottom = math.floor((y + radius) / self.size)

        coords = set([(i, j) for i in range(s_left, s_right)
                      for j in range(s_top, s_bottom)])

        old_coords = self.entity_map[id] - coords
        new_coords = coords - self.entity_map[id]

        self.entity_map[id] = coords
        for coord in old_coords:
            self.map[coord].remove(id)

        for coord in new_coords:
            self.map[coord].add(id)
        return coords

    def remove(self, id):
        for coord in self.entity_map[id]:
            self.map[coord].remove(id)
        del self.entity_map[id]

    def neighbours(self, id):
        ns = set()
        for coord in self.entity_map[id]:
            ns += self.map[coord]
        return ns

    def neighbours_coords(self, x, y):
        s_x, s_y = math.floor(x / self.size), math.floor(y / self.size)
        return self.map[(s_x, s_y)]
