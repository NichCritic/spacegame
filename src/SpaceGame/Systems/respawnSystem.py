from Systems.system import System
import math
import logging
import time
import json

class RespawnSystem(System):

    mandatory = ["spawn", "respawn"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        now = time.time() * 1000
        if now  - node.spawn.start_time > node.respawn.respawn_time:
            icomp = json.loads(node.respawn.spec)
            # import pdb
            # pdb.set_trace()
            for component, data in icomp.items():
                node.add_or_attach_component(component, data)

            node.remove_component('spawn')
