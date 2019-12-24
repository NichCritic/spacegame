from Systems.system import System
import logging


class ProximityTargetSystem(System):

    mandatory = ["proximity", "proximity_target_behaviour"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def handle(self, node):

        if len(node.proximity.proximity_map.keys()) > 0:
            keys = set(node.proximity.proximity_map.keys()) - set(node.proximity_target_behaviour.exclusion_list)
            closest = min(keys,
                          key=lambda n: node.proximity.proximity_map[n])

            # logging.info(node.proximity.proximity_map)
            # logging.info(f"targetting {closest}")

            node.add_or_update_component("target", {
                "target_id": closest
            })
            node.target.id = closest

        elif node.entity_has("target"):
            node.remove_component("target")
