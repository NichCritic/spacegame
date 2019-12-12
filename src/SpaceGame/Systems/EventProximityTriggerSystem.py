from Systems.system import System
import logging


class EventProximityTriggerSystem(System):

    mandatory = ["event", "proximity", "event_proximity_trigger", "area"]
    optional = []
    handles = []

    def __init__(self, node_factory):
        self.node_factory = node_factory
        self.sim_time = 0

    def trigger(self, proxy_map, n, radius):
        is_player = self.node_factory.create_node(
            n, [], []).entity_has('player_controlled')
        is_in_range = proxy_map[n] < radius
        return is_player and is_in_range

    def trigger_condition(self, proxy_map, radius):
        return any([self.trigger(proxy_map, n, radius) for n in proxy_map.keys()])

    def handle(self, node):
        proxy_map = node.proximity.proximity_map
        radius = node.area.radius
        if len(node.proximity.proximity_map.keys()) > 0:
            player_inside = self.trigger_condition(proxy_map, radius)

            if player_inside:
                node.add_or_update_component("event_active", {})
            elif node.entity_has("event_active"):
                node.remove_component("event_active")

        elif node.entity_has("event_active"):
            node.remove_component("event_active")
