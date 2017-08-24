from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class PuttingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "putting", "container"])

    def create_av_event_data(self, location, putting, target, **kwargs):
        event = AVEvent("putting", None, location.detach(),
                        putting.entity_id, putting.format, target, **kwargs)
        return event


    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            subject, object = tuple(node.putting.targets.values())
            sub_node = self.node_factory.create_node(subject, ["names", "container"])
            obj_node = self.node_factory.create_node(object, ["names", "container"])

            sub_node.container.parent_id = obj_node.container.id
            sub_node.container.type = node.putting.type

            room_node = self.node_factory.create_node(
                        node.location.room, [])
            av_event_data = self.create_av_event_data(
                        node.location, node.putting, None, subject = subject, object = object)
            print("Taking system got message from "+node.id)
            room_node.add_or_attach_component("av_events", None)
            room_node.av_events.events.append(av_event_data)




            
                    

            node.remove_component("putting")