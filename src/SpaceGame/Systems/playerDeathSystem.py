from Systems.system import System
import math
import logging
import time
from gamedata.ships import default_ship


class PlayerDeathSystem(System):

    mandatory = ["player_controlled", "dead", "position"]
    optional = ["quests"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def handle(self, node):
        # Create a new dead node in the same position as the previous node
        self.node_factory.create_new_node({
            "position": {"x": node.position.x, "y": node.position.y},
            "dead": {}
        })

        pid = node.player_controlled.pid
        quests = None
        if node.has("quests"):
            quests = node.quests.quests
        # Delete the player then move them to spawn
        node.remove_all_components()
        node.add_or_attach_component("player_controlled", {"pid": pid})
        default_ship(node)
        node.add_or_attach_component("quests", {"quests":quests})
