from Systems.system import System
import logging


class ProximityTargetSystem(System):

    mandatory = ["proximity", "proximity_target_behaviour"]
    optional = ["no_target_allies", "allies"]
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def get_allies(self, keys, team):
        allies = []
        for key in keys:
            n = self.node_factory.create_node(key, [], ["allies"])
            if n.has("allies") and n.allies.team == team:
                allies.append(key)
        logging.info(f"Allies: {allies}")
        return allies

    def handle(self, node):

        if len(node.proximity.proximity_map.keys()) > 0:
            keys = set(node.proximity.proximity_map.keys()) - \
                set(node.proximity_target_behaviour.exclusion_list)

            if node.has("no_target_allies") and node.has("allies"):
                keys -= set(self.get_allies(keys, node.allies.team))

            closest = min(keys,
                          key=lambda n: node.proximity.proximity_map[n])

            # logging.info(node.proximity.proximity_map)
            # logging.info(f"targetting {closest}, dist:
            # {node.proximity.proximity_map[closest]}")

            node.add_or_update_component("target", {
                "target_id": closest
            })
            node.target.id = closest

        elif node.entity_has("target"):
            node.remove_component("target")
