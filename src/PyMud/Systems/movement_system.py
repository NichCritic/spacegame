from Systems.system import System
from Systems.av_event_mixin import AVEventMixin
from Systems.NetworkMessageSystem import NetworkMessage


class MovingSystem(System, AVEventMixin):
    manditory = ["names", "location", "moving", "container"]
    handles = ["moving"]

    def handle(self, node):
        for t_name, t_id in node.moving.target.items():
            node.add_or_update_component(
                "close_to", {"n_id": t_id})
            self.av_event(node, {
                "target": t_name,
                "player": node.names.name
            }, node.moving.format)
