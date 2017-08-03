from Systems.AVEvent import AVEvent
from Systems.NetworkMessageSystem import NetworkMessage


class WritingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''

    def __init__(self, node_factory):
        self.node_factory = node_factory

    def get_nodes(self):
        return self.node_factory.create_node_list(["writing", "location"])

    def create_av_event_data(self, location, writing, target):
        event = AVEvent("writing", None, location.detach(),
                        writing.entity_id, writing.format, target)
        return event


    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            for t_name, t_id in node.writing.target.items():
                print(t_id)
                target_object = self.node_factory.create_node(
                    t_id, ['names'], ['runes'])
                
                if not target_object.has('runes'):
                    target_object.add_or_attach_component("runes", {"active":False, "runes_list":[]})
                target_object.runes.runes_list = target_object.runes.runes_list + [node.writing.rune] 
                
                room_node = self.node_factory.create_node(
                    node.location.room, [])
                av_event_data = self.create_av_event_data(
                    node.location, node.writing, t_id)
                print("Writing system got message from "+node.id)
                room_node.add_or_attach_component("av_events", None)
                room_node.av_events.events.append(av_event_data)

            
                    

            node.remove_component("writing")