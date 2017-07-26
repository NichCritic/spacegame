from Systems.AVEvent import AVEvent
from scripts import scripts
import time

class HoldTriggerSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["held_by", "on_hold"], ["on_hold_timeout"])

    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            now = time.time()
            if not node.has('on_hold_timeout') or now - node.on_hold_timeout.last_trigger > node.on_hold.timeout:
                data = node.on_hold.data
                data['node_factory'] = self.node_factory
                data['on_hold'] = node.on_hold
                data["held_entity_id"] = node.id
                data["holding_entity_id"] = node.held_by.holding_entity_id
                callback = scripts[node.on_hold.callback]
                callback(**data)
                node.add_or_update_component("on_hold_timeout", {"last_trigger": now})

            
