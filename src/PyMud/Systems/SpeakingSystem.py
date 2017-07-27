from Systems.AVEvent import AVEvent

class SpeakingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
        
    
    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "speaking"])
            
    def create_av_event_data(self, location, speaking):
        if speaking.target:
            target = speaking.target.keys()[0]
        else:
            target = None
        event = AVEvent("speaking", speaking.text, location.detach(), speaking.entity_id, speaking.format, target)
        return event
        
    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            room_node = self.node_factory.create_node(node.location.room, [])
            av_event_data = self.create_av_event_data(node.location, node.speaking) 
            print("Speaking system got message from "+node.id)
            room_node.add_or_attach_component("av_events", None)
            room_node.av_events.events.append(av_event_data)
            node.remove_component("speaking")
            