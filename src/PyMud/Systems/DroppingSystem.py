from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class DroppingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "dropping", "container"])

    def create_av_event_data(self, location, dropping, target):
        event = AVEvent("dropping", None, location.detach(),
                        dropping.entity_id, dropping.format, target)
        return event

    def object_is_held_by(self, object, held_by):
        if object.container.type == 'held':
            if object.container.parent_id == held_by.container.id:
                return True
        return False


    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            for t_name, t_id in node.dropping.target.items():
                print(t_id)

                dropped_object = self.node_factory.create_node(t_id, ['names', 'container'])
                if self.object_is_held_by(dropped_object, node):

                    room_node = self.node_factory.create_node(
                        node.location.room, [])
                    av_event_data = self.create_av_event_data(
                        node.location, node.dropping, t_id)
                    print("Dropping system got message from "+node.id)
                    room_node.add_or_attach_component("av_events", None)
                    room_node.av_events.events.append(av_event_data)

                    #Put the object in the same room as the node
                    dropped_object.container.parent_id = node.container.parent_id
                    dropped_object.container.type = 'in'


            node.remove_component("dropping")
