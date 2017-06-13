'''
Created on 2013-11-27

@author: Nich
'''

from collections import defaultdict
from PyMud.Systems.NetworkMessageSystem import NetworkMessage

def walk_tree_bf(starting_node):
    queue = []
    visited = set()
    
    queue.append(starting_node)
    visited.add(starting_node)
    
    for n in queue:
        yield n
        for node in n.get_neighbours():
            if node not in visited:
                queue.append(node)
                visited.add(node) 


class DescriptionSystem(object):
    '''
    Builds the description of a room from the description of the locations
    
    '''
    def __init__(self, node_factory):
        self.node_factory = node_factory
        
    def describe_object(self, object_id):
        object_node = self.node_factory.create_node(object_id, ["description"])
        return "{description} \n".format(description = object_node.description.description)
        
        
    def describe_room(self, room_id):
        description = ""
        room_node = self.node_factory.create_node(room_id, ["room", "names", "container"])
        description += room_node.names.name+"\n"
        for o in room_node.container.children:
            description += self.describe_object(o.entity_id)
                
        return description
    


class NetworkDescriptionSystem():
    
    def __init__(self, node_factory, desc_system):
        self.node_factory = node_factory
        self.desc_system = desc_system
        
    def get_nodes(self):
        return self.node_factory.create_node_list(["looking", "location"])
    
    def process(self):
        nodes = self.get_nodes()    
        for node in nodes:
            msg = ""
            if node.looking.target is None:
                msg = self.desc_system.describe_room(node.location.room)
            else:
                msg = self.desc_system.describe_object(node.looking.target)
            out_msg = NetworkMessage(node.id, msg)
            node.add_or_attach_component("network_messages", {})
            node.network_messages.msg.append(out_msg)
            node.remove_component("looking")
            
            
                
                    
                    
                    
                    
                
if __name__ == "__main__":
    from PyMud.startup_scripts import setup_db, ObjectProvider, components
    Session = setup_db()
    op = ObjectProvider(Session)
    
    rds = DescriptionSystem(op.node_factory)
    
    

'''
class NetworkRoomDescriptionSystem(object):
    
    Builds the description of a room from the description of the locations
    
    
    def __init__(self, MessageQueue, node_factory, messanger_queue):
        self.message_queue = MessageQueue
        self.av_nodes = []
        self.node_factory = node_factory
        self.messanger_queue = messanger_queue
   
   
    def aggregate_by_contents(self, start_loc):
        contents = defaultdict(set)
        for loc in walk_tree_bf(start_loc):
            if not loc.contents:
                contents["nothing"].add(loc)
            else:
                print(loc.contents)
                for _, c in loc.contents.items():
                    contents[c.type].add(loc)
        return contents

    def display_room(self, start_loc):
        #aggregate by contents
        contents = self.aggregate_by_contents(start_loc)
        results = ""
        for k, v in contents.items():
            results += k +", "+(str(v))+"\n"
        return results
   
    def process_messages(self):
        
        while self.av_message_queue.qsize() >= 1:
            message = self.message_queue.get()
            
            
            out_msg = NetworkMessage(message.id, message.message.format(player = message.source_id, target = message.target_id, text = message.text))
            self.messanger_queue.put(out_msg)
                        
'''

   

        