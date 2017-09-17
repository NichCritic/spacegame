from Systems.system import System
from Systems.av_event_mixin import AVEventMixin
from Systems.NetworkMessageSystem import NetworkMessage


class PuttingSystem(System, AVEventMixin):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''
    manditory = ["names", "location", "putting", "container"]
    handles = ['putting']

    def handle(self, node):
        subject, object = tuple(node.putting.targets.values())
        sub_node = self.node_factory.create_node(
            subject, ["names", "container"])
        obj_node = self.node_factory.create_node(
            object, ["names", "container"])

        sub_node.container.parent_id = obj_node.container.id
        sub_node.container.type = node.putting.type

        self.av_event(node, {
            "subject": sub_node.names.name,
            "object": obj_node.names.name,
            "player": node.names.name
        }, node.putting.format)
