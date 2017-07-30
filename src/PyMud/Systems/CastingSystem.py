from Systems.AVEvent import AVEvent

class CastingSystem(object):
    '''
    Generates annoying ticks that everyone with a network connection gets (Debug)
    '''


    def __init__(self, node_factory, spells):
        self.node_factory = node_factory
        self.spells = spells
        
    
    def get_nodes(self):
        return self.node_factory.create_node_list(["location", "casting"])
            
    def create_av_event_data(self, location, casting):
        if casting.target:
            target = list(casting.target.items())[0][1]
        else:
            target = None
        event = AVEvent("casting", casting.spell, location.detach(), casting.entity_id, casting.format, target)
        return event
        
    def process(self):
        self.nodes = self.get_nodes()
        for node in self.nodes:
            room_node = self.node_factory.create_node(node.location.room, [])
            av_event_data = self.create_av_event_data(node.location, node.casting) 
            print("Casting system got message from "+node.id)
            room_node.add_or_attach_component("av_events", None)
            room_node.av_events.events.append(av_event_data)

            target_id = list(node.casting.target.items())[0][1]
            target_node = self.node_factory.create_node(target_id, [])

            spellfn = self.spells[node.casting.spell]["function"]

            spellfn(node, room_node, target_node)

            node.remove_component("casting")
            