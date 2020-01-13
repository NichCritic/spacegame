from Systems.system import System
import math
import logging
import time


class DeathRespawnSystem(System):

    mandatory = ["dead", "respawn"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        now = time.time() * 1000
        self.node_factory.create_new_node({
            "respawn": {"respawn_time": node.respawn.respawn_time, "spec":node.respawn.spec},
            "spawn": {"start_time":now}
        })