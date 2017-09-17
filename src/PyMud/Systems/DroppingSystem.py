from Systems.av_event_mixin import AVEventMixin
from Systems.system import System
from Systems.NetworkMessageSystem import NetworkMessage


class DroppingSystem(System, AVEventMixin):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    manditory = ["names", "location", "dropping", "container"]
    handles = ["dropping"]

    def object_is_held_by(self, object, held_by):
        if object.container.type == 'held':
            if object.container.parent_id == held_by.container.id:
                return True
        return False

    def handle(self, node):
        for t_name, t_id in node.dropping.target.items():
            dropped_object = self.node_factory.create_node(
                t_id, ['names', 'container'])
            if self.object_is_held_by(dropped_object, node):

                room_node = self.node_factory.create_node(
                    node.location.room, [])

                self.av_event(node, {'target': dropped_object.names.name,
                                     'player': node.names.name}, node.dropping.format)
                # Put the object in the same room as the node
                dropped_object.container.parent_id = node.container.parent_id
                dropped_object.container.type = 'in'
