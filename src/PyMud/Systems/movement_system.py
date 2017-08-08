from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class MovingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "moving", "container"])

    def create_av_event_data(self, location, moving, target):
        event = AVEvent("moving", None, location.detach(),
                        moving.entity_id, moving.format, target)
        return event


    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            for t_name, t_id in node.moving.target.items():
                node.add_or_update_component(
                    "close_to", {"n_id": t_id})

                room_node = self.node_factory.create_node(
                    node.location.room, [])
                av_event_data = self.create_av_event_data(
                    node.location, node.moving, t_id)
                print("Moving system got message from "+node.id)
                room_node.add_or_attach_component("av_events", None)
                room_node.av_events.events.append(av_event_data)

            node.remove_component("moving")