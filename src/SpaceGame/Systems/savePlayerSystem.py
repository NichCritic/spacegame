from Systems.system import System
import math
import time
import random
import objects.item as Items
import json
import logging


class SavePlayerSystem(System):

    mandatory = ["player_controlled"]
    optional = []
    handles = []

    def __init__(self, node_factory, session_manager):
        self.node_factory = node_factory
        self.session_manager = session_manager
        self.last_time = time.time()
        self.acc_time = 0

    def handle(self, node):
        t = time.time()
        dt = t - self.last_time
        self.acc_time += dt
        if self.acc_time < 5:
            self.last_time = t
            return
        self.acc_time = 0

        logging.info(node)
        with self.session_manager.get_session() as session:
            s_node = self.node_factory.create_node(
                node.id, [], ["position", "applied_upgrades", "inventory", "money", "health"])
            logging.info(s_node.to_dict())
            node.add_or_update_component("instance_components", {
                                         "components": json.dumps(s_node.to_dict())})

        self.last_time = t
