from Systems.system import System
import logging


class PlayerProximityTargetSystem(System):

    mandatory = ["proximity", "player_proximity_target_behaviour"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def get_players(self, keys):
        # logging.info(keys)
        nodes = self.node_factory.create_node_list(["player_controlled"], [], entity_ids = keys)
        return [n.id for n in nodes]

    def handle(self, node):
        players_in_area = self.get_players(node.proximity.proximity_map.keys())
        if len(players_in_area) > 0:
            closest = min(players_in_area,
                          key=lambda n: node.proximity.proximity_map[n])

            # logging.info(node.proximity.proximity_map)
            # logging.info(f"targetting {closest}")

            node.add_or_update_component("target", {
                "target_id": closest
            })
            node.target.id = closest

        elif node.entity_has("target"):
            node.remove_component("target")
