from Systems.AVEvent import AVEvent
from Systems.system import System
from scripts import scripts
import time


class HoldTriggerSystem(System):
    manditory = ["container", "on_hold"]
    optional = ["on_hold_timeout"]

    def handle(self, node):
        print(f"{node.id}, {node.on_hold.callback}, {node.container.type}")
        now = time.time()
        if not node.has('on_hold_timeout') or now - node.on_hold_timeout.last_trigger > node.on_hold.timeout:
            if node.container.type == 'held':
                data = node.on_hold.data
                data['node_factory'] = self.node_factory
                data['on_hold'] = node.on_hold
                data["held_entity_id"] = node.id
                data["holding_entity_id"] = node.container.parent.entity_id
                callback = scripts[node.on_hold.callback]
                callback(**data)
                node.add_or_update_component(
                    "on_hold_timeout", {"last_trigger": now})
