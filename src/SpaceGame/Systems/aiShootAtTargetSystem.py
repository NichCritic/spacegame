from Systems.system import System
import math
import time
import logging


class AIShootAtTargetSystem(System):

    manditory = ["shoot_at_target", "target", "rotation", "position"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):
        pass
