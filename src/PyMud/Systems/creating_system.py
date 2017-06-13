'''
Created on 2014-03-31

@author: Nich
'''


class CreatingSystem(object):
    '''
    Create a new entity in the node's current room
    '''


    def __init__(self, node_factory):
        self.node_factory = node_factory
        
        
    def get_nodes(self):
        nodes = self.node_factory.create_node_list(["creating", "location"])
        return nodes
    
    def process(self):
        
        nodes = self.get_nodes()
        for node in nodes:
            room = node.location.room
            room_node = self.node_factory.create_node(room, ["container"])
            x = node.location.x
            y = node.location.y
            z = node.location.z
            self.node_factory.create_new_node({
                                       "container":{"parent_id":room_node.container.id},
                                       "location":{"room": room, "x":x, "y":y, "z":z},
                                       "description":{"description":"A new glowing entity"},
                                       "names":{}, 
                                       
                                       })
            
            #TODO Notification
            node.remove_component("creating")
            
        